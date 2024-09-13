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
from typing import TYPE_CHECKING, Callable, TypeVar, Awaitable, Union, overload
from typing_extensions import ParamSpec

if TYPE_CHECKING:
    from ..rest import AsyncHttpResponse as RestAsyncHttpResponse

P = ParamSpec("P")
T = TypeVar("T")


@overload
async def await_result(func: Callable[P, Awaitable[T]], *args: P.args, **kwargs: P.kwargs) -> T: ...


@overload
async def await_result(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T: ...


async def await_result(func: Callable[P, Union[T, Awaitable[T]]], *args: P.args, **kwargs: P.kwargs) -> T:
    """If func returns an awaitable, await it.

    :param func: The function to run.
    :type func: callable
    :param args: The positional arguments to pass to the function.
    :type args: list
    :rtype: any
    :return: The result of the function
    """
    result = func(*args, **kwargs)
    if isinstance(result, Awaitable):
        return await result
    return result


async def handle_no_stream_rest_response(response: "RestAsyncHttpResponse") -> None:
    """Handle reading and closing of non stream rest responses.
    For our new rest responses, we have to call .read() and .close() for our non-stream
    responses. This way, we load in the body for users to access.

    :param response: The response to read and close.
    :type response: ~azure.core.rest.AsyncHttpResponse
    """
    try:
        await response.read()
        await response.close()
    except Exception as exc:
        await response.close()
        raise exc
