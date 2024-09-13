# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------
"""
This module is the requests implementation of Pipeline ABC
"""
import logging
from urllib.parse import urlparse
from typing import Optional, TypeVar, Dict, Any, Union, Type
from typing_extensions import Literal

from azure.core.exceptions import TooManyRedirectsError
from azure.core.pipeline import PipelineResponse, PipelineRequest
from azure.core.pipeline.transport import (
    HttpResponse as LegacyHttpResponse,
    HttpRequest as LegacyHttpRequest,
    AsyncHttpResponse as LegacyAsyncHttpResponse,
)
from azure.core.rest import HttpResponse, HttpRequest, AsyncHttpResponse
from ._base import HTTPPolicy, RequestHistory
from ._utils import get_domain

HTTPResponseType = TypeVar("HTTPResponseType", HttpResponse, LegacyHttpResponse)
AllHttpResponseType = TypeVar(
    "AllHttpResponseType", HttpResponse, LegacyHttpResponse, AsyncHttpResponse, LegacyAsyncHttpResponse
)
HTTPRequestType = TypeVar("HTTPRequestType", HttpRequest, LegacyHttpRequest)
ClsRedirectPolicy = TypeVar("ClsRedirectPolicy", bound="RedirectPolicyBase")

_LOGGER = logging.getLogger(__name__)


def domain_changed(original_domain: Optional[str], url: str) -> bool:
    """Checks if the domain has changed.
    :param str original_domain: The original domain.
    :param str url: The new url.
    :rtype: bool
    :return: Whether the domain has changed.
    """
    domain = get_domain(url)
    if not original_domain:
        return False
    if original_domain == domain:
        return False
    return True


class RedirectPolicyBase:

    REDIRECT_STATUSES = frozenset([300, 301, 302, 303, 307, 308])

    REDIRECT_HEADERS_BLACKLIST = frozenset(["Authorization"])

    def __init__(self, **kwargs: Any) -> None:
        self.allow: bool = kwargs.get("permit_redirects", True)
        self.max_redirects: int = kwargs.get("redirect_max", 30)

        remove_headers = set(kwargs.get("redirect_remove_headers", []))
        self._remove_headers_on_redirect = remove_headers.union(self.REDIRECT_HEADERS_BLACKLIST)
        redirect_status = set(kwargs.get("redirect_on_status_codes", []))
        self._redirect_on_status_codes = redirect_status.union(self.REDIRECT_STATUSES)
        super(RedirectPolicyBase, self).__init__()

    @classmethod
    def no_redirects(cls: Type[ClsRedirectPolicy]) -> ClsRedirectPolicy:
        """Disable redirects.

        :return: A redirect policy with redirects disabled.
        :rtype: ~azure.core.pipeline.policies.RedirectPolicy or ~azure.core.pipeline.policies.AsyncRedirectPolicy
        """
        return cls(permit_redirects=False)

    def configure_redirects(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Configures the redirect settings.

        :param options: Keyword arguments from context.
        :type options: dict
        :return: A dict containing redirect settings and a history of redirects.
        :rtype: dict
        """
        return {
            "allow": options.pop("permit_redirects", self.allow),
            "redirects": options.pop("redirect_max", self.max_redirects),
            "history": [],
        }

    def get_redirect_location(
        self, response: PipelineResponse[Any, AllHttpResponseType]
    ) -> Union[str, None, Literal[False]]:
        """Checks for redirect status code and gets redirect location.

        :param response: The PipelineResponse object
        :type response: ~azure.core.pipeline.PipelineResponse
        :return: Truthy redirect location string if we got a redirect status
         code and valid location. ``None`` if redirect status and no
         location. ``False`` if not a redirect status code.
        :rtype: str or bool or None
        """
        if response.http_response.status_code in [301, 302]:
            if response.http_request.method in [
                "GET",
                "HEAD",
            ]:
                return response.http_response.headers.get("location")
            return False
        if response.http_response.status_code in self._redirect_on_status_codes:
            return response.http_response.headers.get("location")

        return False

    def increment(
        self, settings: Dict[str, Any], response: PipelineResponse[Any, AllHttpResponseType], redirect_location: str
    ) -> bool:
        """Increment the redirect attempts for this request.

        :param dict settings: The redirect settings
        :param response: A pipeline response object.
        :type response: ~azure.core.pipeline.PipelineResponse
        :param str redirect_location: The redirected endpoint.
        :return: Whether further redirect attempts are remaining.
         False if exhausted; True if more redirect attempts available.
        :rtype: bool
        """
        # TODO: Revise some of the logic here.
        settings["redirects"] -= 1
        settings["history"].append(RequestHistory(response.http_request, http_response=response.http_response))

        redirected = urlparse(redirect_location)
        if not redirected.netloc:
            base_url = urlparse(response.http_request.url)
            response.http_request.url = "{}://{}/{}".format(
                base_url.scheme, base_url.netloc, redirect_location.lstrip("/")
            )
        else:
            response.http_request.url = redirect_location
        if response.http_response.status_code == 303:
            response.http_request.method = "GET"
        for non_redirect_header in self._remove_headers_on_redirect:
            response.http_request.headers.pop(non_redirect_header, None)
        return settings["redirects"] >= 0


class RedirectPolicy(RedirectPolicyBase, HTTPPolicy[HTTPRequestType, HTTPResponseType]):
    """A redirect policy.

    A redirect policy in the pipeline can be configured directly or per operation.

    :keyword bool permit_redirects: Whether the client allows redirects. Defaults to True.
    :keyword int redirect_max: The maximum allowed redirects. Defaults to 30.

    .. admonition:: Example:

        .. literalinclude:: ../samples/test_example_sync.py
            :start-after: [START redirect_policy]
            :end-before: [END redirect_policy]
            :language: python
            :dedent: 4
            :caption: Configuring a redirect policy.
    """

    def send(self, request: PipelineRequest[HTTPRequestType]) -> PipelineResponse[HTTPRequestType, HTTPResponseType]:
        """Sends the PipelineRequest object to the next policy.
        Uses redirect settings to send request to redirect endpoint if necessary.

        :param request: The PipelineRequest object
        :type request: ~azure.core.pipeline.PipelineRequest
        :return: Returns the PipelineResponse or raises error if maximum redirects exceeded.
        :rtype: ~azure.core.pipeline.PipelineResponse
        :raises: ~azure.core.exceptions.TooManyRedirectsError if maximum redirects exceeded.
        """
        retryable: bool = True
        redirect_settings = self.configure_redirects(request.context.options)
        original_domain = get_domain(request.http_request.url) if redirect_settings["allow"] else None
        while retryable:
            response = self.next.send(request)
            redirect_location = self.get_redirect_location(response)
            if redirect_location and redirect_settings["allow"]:
                retryable = self.increment(redirect_settings, response, redirect_location)
                request.http_request = response.http_request
                if domain_changed(original_domain, request.http_request.url):
                    # "insecure_domain_change" is used to indicate that a redirect
                    # has occurred to a different domain. This tells the SensitiveHeaderCleanupPolicy
                    # to clean up sensitive headers. We need to remove it before sending the request
                    # to the transport layer.
                    request.context.options["insecure_domain_change"] = True
                continue
            return response

        raise TooManyRedirectsError(redirect_settings["history"])
