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
import logging
import collections.abc
from typing import (
    Any,
    Awaitable,
    TypeVar,
    AsyncContextManager,
    Generator,
    Generic,
    Optional,
    Type,
    cast,
)
from types import TracebackType
from .configuration import Configuration
from .pipeline import AsyncPipeline
from .pipeline.transport._base import PipelineClientBase
from .pipeline.policies import (
    ContentDecodePolicy,
    DistributedTracingPolicy,
    HttpLoggingPolicy,
    RequestIdPolicy,
    AsyncRetryPolicy,
    SensitiveHeaderCleanupPolicy,
)


HTTPRequestType = TypeVar("HTTPRequestType")
AsyncHTTPResponseType = TypeVar("AsyncHTTPResponseType", bound="AsyncContextManager")

_LOGGER = logging.getLogger(__name__)


class _Coroutine(Awaitable[AsyncHTTPResponseType]):
    """Wrapper to get both context manager and awaitable in place.

    Naming it "_Coroutine" because if you don't await it makes the error message easier:
    >>> result = client.send_request(request)
    >>> result.text()
    AttributeError: '_Coroutine' object has no attribute 'text'

    Indeed, the message for calling a coroutine without waiting would be:
    AttributeError: 'coroutine' object has no attribute 'text'

    This allows the dev to either use the "async with" syntax, or simply the object directly.
    It's also why "send_request" is not declared as async, since it couldn't be both easily.

    "wrapped" must be an awaitable object that returns an object implements the async context manager protocol.

    This permits this code to work for both following requests.

    ```python
    from azure.core import AsyncPipelineClient
    from azure.core.rest import HttpRequest

    async def main():

        request = HttpRequest("GET", "https://httpbin.org/user-agent")
        async with AsyncPipelineClient("https://httpbin.org/") as client:
            # Can be used directly
            result = await client.send_request(request)
            print(result.text())

            # Can be used as an async context manager
            async with client.send_request(request) as result:
                print(result.text())
    ```

    :param wrapped: Must be an awaitable the returns an async context manager that supports async "close()"
    :type wrapped: awaitable[AsyncHTTPResponseType]
    """

    def __init__(self, wrapped: Awaitable[AsyncHTTPResponseType]) -> None:
        super().__init__()
        self._wrapped = wrapped
        # If someone tries to use the object without awaiting, they will get a
        # AttributeError: '_Coroutine' object has no attribute 'text'
        self._response: AsyncHTTPResponseType = cast(AsyncHTTPResponseType, None)

    def __await__(self) -> Generator[Any, None, AsyncHTTPResponseType]:
        return self._wrapped.__await__()

    async def __aenter__(self) -> AsyncHTTPResponseType:
        self._response = await self
        return self._response

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        await self._response.__aexit__(exc_type, exc_value, traceback)


class AsyncPipelineClient(
    PipelineClientBase,
    AsyncContextManager["AsyncPipelineClient"],
    Generic[HTTPRequestType, AsyncHTTPResponseType],
):
    """Service client core methods.

    Builds an AsyncPipeline client.

    :param str base_url: URL for the request.
    :keyword ~azure.core.configuration.Configuration config: If omitted, the standard configuration is used.
    :keyword Pipeline pipeline: If omitted, a Pipeline object is created and returned.
    :keyword list[AsyncHTTPPolicy] policies: If omitted, the standard policies of the configuration object is used.
    :keyword per_call_policies: If specified, the policies will be added into the policy list before RetryPolicy
    :paramtype per_call_policies: Union[AsyncHTTPPolicy, SansIOHTTPPolicy,
        list[AsyncHTTPPolicy], list[SansIOHTTPPolicy]]
    :keyword per_retry_policies: If specified, the policies will be added into the policy list after RetryPolicy
    :paramtype per_retry_policies: Union[AsyncHTTPPolicy, SansIOHTTPPolicy,
        list[AsyncHTTPPolicy], list[SansIOHTTPPolicy]]
    :keyword AsyncHttpTransport transport: If omitted, AioHttpTransport is used for asynchronous transport.
    :return: An async pipeline object.
    :rtype: ~azure.core.pipeline.AsyncPipeline

    .. admonition:: Example:

        .. literalinclude:: ../samples/test_example_async.py
            :start-after: [START build_async_pipeline_client]
            :end-before: [END build_async_pipeline_client]
            :language: python
            :dedent: 4
            :caption: Builds the async pipeline client.
    """

    def __init__(
        self,
        base_url: str,
        *,
        pipeline: Optional[AsyncPipeline[HTTPRequestType, AsyncHTTPResponseType]] = None,
        config: Optional[Configuration[HTTPRequestType, AsyncHTTPResponseType]] = None,
        **kwargs: Any,
    ):
        super(AsyncPipelineClient, self).__init__(base_url)
        self._config: Configuration[HTTPRequestType, AsyncHTTPResponseType] = config or Configuration(**kwargs)
        self._base_url = base_url
        self._pipeline = pipeline or self._build_pipeline(self._config, **kwargs)

    async def __aenter__(self) -> AsyncPipelineClient[HTTPRequestType, AsyncHTTPResponseType]:
        await self._pipeline.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        await self._pipeline.__aexit__(exc_type, exc_value, traceback)

    async def close(self) -> None:
        await self.__aexit__()

    def _build_pipeline(
        self,
        config: Configuration[HTTPRequestType, AsyncHTTPResponseType],
        *,
        policies=None,
        per_call_policies=None,
        per_retry_policies=None,
        **kwargs,
    ) -> AsyncPipeline[HTTPRequestType, AsyncHTTPResponseType]:
        transport = kwargs.get("transport")
        per_call_policies = per_call_policies or []
        per_retry_policies = per_retry_policies or []

        if policies is None:  # [] is a valid policy list
            policies = [
                config.request_id_policy or RequestIdPolicy(**kwargs),
                config.headers_policy,
                config.user_agent_policy,
                config.proxy_policy,
                ContentDecodePolicy(**kwargs),
            ]
            if isinstance(per_call_policies, collections.abc.Iterable):
                policies.extend(per_call_policies)
            else:
                policies.append(per_call_policies)

            policies.extend(
                [
                    config.redirect_policy,
                    config.retry_policy,
                    config.authentication_policy,
                    config.custom_hook_policy,
                ]
            )
            if isinstance(per_retry_policies, collections.abc.Iterable):
                policies.extend(per_retry_policies)
            else:
                policies.append(per_retry_policies)

            policies.extend(
                [
                    config.logging_policy,
                    DistributedTracingPolicy(**kwargs),
                    SensitiveHeaderCleanupPolicy(**kwargs) if config.redirect_policy else None,
                    config.http_logging_policy or HttpLoggingPolicy(**kwargs),
                ]
            )
        else:
            if isinstance(per_call_policies, collections.abc.Iterable):
                per_call_policies_list = list(per_call_policies)
            else:
                per_call_policies_list = [per_call_policies]
            per_call_policies_list.extend(policies)
            policies = per_call_policies_list
            if isinstance(per_retry_policies, collections.abc.Iterable):
                per_retry_policies_list = list(per_retry_policies)
            else:
                per_retry_policies_list = [per_retry_policies]
            if len(per_retry_policies_list) > 0:
                index_of_retry = -1
                for index, policy in enumerate(policies):
                    if isinstance(policy, AsyncRetryPolicy):
                        index_of_retry = index
                if index_of_retry == -1:
                    raise ValueError(
                        "Failed to add per_retry_policies; no RetryPolicy found in the supplied list of policies. "
                    )
                policies_1 = policies[: index_of_retry + 1]
                policies_2 = policies[index_of_retry + 1 :]
                policies_1.extend(per_retry_policies_list)
                policies_1.extend(policies_2)
                policies = policies_1

        if not transport:
            # Use private import for better typing, mypy and pyright don't like PEP562
            from .pipeline.transport._aiohttp import AioHttpTransport

            transport = AioHttpTransport(**kwargs)

        return AsyncPipeline[HTTPRequestType, AsyncHTTPResponseType](transport, policies)

    async def _make_pipeline_call(self, request: HTTPRequestType, **kwargs) -> AsyncHTTPResponseType:
        return_pipeline_response = kwargs.pop("_return_pipeline_response", False)
        pipeline_response = await self._pipeline.run(request, **kwargs)  # pylint: disable=protected-access
        if return_pipeline_response:
            return pipeline_response  # type: ignore  # This is a private API we don't want to type in signature
        return pipeline_response.http_response

    def send_request(
        self, request: HTTPRequestType, *, stream: bool = False, **kwargs: Any
    ) -> Awaitable[AsyncHTTPResponseType]:
        """Method that runs the network request through the client's chained policies.

        >>> from azure.core.rest import HttpRequest
        >>> request = HttpRequest('GET', 'http://www.example.com')
        <HttpRequest [GET], url: 'http://www.example.com'>
        >>> response = await client.send_request(request)
        <AsyncHttpResponse: 200 OK>

        :param request: The network request you want to make. Required.
        :type request: ~azure.core.rest.HttpRequest
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call. Does not do error handling on your response.
        :rtype: ~azure.core.rest.AsyncHttpResponse
        """
        wrapped = self._make_pipeline_call(request, stream=stream, **kwargs)
        return _Coroutine(wrapped=wrapped)
