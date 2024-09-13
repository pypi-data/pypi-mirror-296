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
from __future__ import annotations
from typing import Union, Optional, Any, Generic, TypeVar, TYPE_CHECKING

HTTPResponseType = TypeVar("HTTPResponseType")
HTTPRequestType = TypeVar("HTTPRequestType")

if TYPE_CHECKING:
    from .pipeline.policies import HTTPPolicy, AsyncHTTPPolicy, SansIOHTTPPolicy

    AnyPolicy = Union[
        HTTPPolicy[HTTPRequestType, HTTPResponseType],
        AsyncHTTPPolicy[HTTPRequestType, HTTPResponseType],
        SansIOHTTPPolicy[HTTPRequestType, HTTPResponseType],
    ]


class Configuration(Generic[HTTPRequestType, HTTPResponseType]):  # pylint: disable=too-many-instance-attributes
    """Provides the home for all of the configurable policies in the pipeline.

    A new Configuration object provides no default policies and does not specify in what
    order the policies will be added to the pipeline. The SDK developer must specify each
    of the policy defaults as required by the service and use the policies in the
    Configuration to construct the pipeline correctly, as well as inserting any
    unexposed/non-configurable policies.

    :ivar headers_policy: Provides parameters for custom or additional headers to be sent with the request.
    :ivar proxy_policy: Provides configuration parameters for proxy.
    :ivar redirect_policy: Provides configuration parameters for redirects.
    :ivar retry_policy: Provides configuration parameters for retries in the pipeline.
    :ivar custom_hook_policy: Provides configuration parameters for a custom hook.
    :ivar logging_policy: Provides configuration parameters for logging.
    :ivar http_logging_policy: Provides configuration parameters for HTTP specific logging.
    :ivar user_agent_policy: Provides configuration parameters to append custom values to the
     User-Agent header.
    :ivar authentication_policy: Provides configuration parameters for adding a bearer token Authorization
     header to requests.
    :ivar request_id_policy: Provides configuration parameters for adding a request id to requests.
    :keyword polling_interval: Polling interval while doing LRO operations, if Retry-After is not set.

    .. admonition:: Example:

        .. literalinclude:: ../samples/test_example_config.py
            :start-after: [START configuration]
            :end-before: [END configuration]
            :language: python
            :caption: Creates the service configuration and adds policies.
    """

    def __init__(self, **kwargs: Any) -> None:
        # Headers (sent with every request)
        self.headers_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Proxy settings (Currently used to configure transport, could be pipeline policy instead)
        self.proxy_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Redirect configuration
        self.redirect_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Retry configuration
        self.retry_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Custom hook configuration
        self.custom_hook_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Logger configuration
        self.logging_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Http logger configuration
        self.http_logging_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # User Agent configuration
        self.user_agent_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Authentication configuration
        self.authentication_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Request ID policy
        self.request_id_policy: Optional[AnyPolicy[HTTPRequestType, HTTPResponseType]] = None

        # Polling interval if no retry-after in polling calls results
        self.polling_interval: float = kwargs.get("polling_interval", 30)


class ConnectionConfiguration:
    """HTTP transport connection configuration settings.

    Common properties that can be configured on all transports. Found in the
    Configuration object.

    :keyword float connection_timeout: A single float in seconds for the connection timeout. Defaults to 300 seconds.
    :keyword float read_timeout: A single float in seconds for the read timeout. Defaults to 300 seconds.
    :keyword connection_verify: SSL certificate verification. Enabled by default. Set to False to disable,
     alternatively can be set to the path to a CA_BUNDLE file or directory with certificates of trusted CAs.
    :paramtype connection_verify: bool or str
    :keyword str connection_cert: Client-side certificates. You can specify a local cert to use as client side
     certificate, as a single file (containing the private key and the certificate) or as a tuple of both files' paths.
    :keyword int connection_data_block_size: The block size of data sent over the connection. Defaults to 4096 bytes.

    .. admonition:: Example:

        .. literalinclude:: ../samples/test_example_config.py
            :start-after: [START connection_configuration]
            :end-before: [END connection_configuration]
            :language: python
            :dedent: 4
            :caption: Configuring transport connection settings.
    """

    def __init__(
        self,  # pylint: disable=unused-argument
        *,
        connection_timeout: float = 300,
        read_timeout: float = 300,
        connection_verify: Union[bool, str] = True,
        connection_cert: Optional[str] = None,
        connection_data_block_size: int = 4096,
        **kwargs: Any,
    ) -> None:
        self.timeout = connection_timeout
        self.read_timeout = read_timeout
        self.verify = connection_verify
        self.cert = connection_cert
        self.data_block_size = connection_data_block_size
