# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from __future__ import absolute_import
from collections.abc import Mapping

from io import BytesIO
from email.message import Message
from email.policy import HTTP
from email import message_from_bytes as message_parser
import os
from typing import (
    TYPE_CHECKING,
    cast,
    IO,
    Union,
    Tuple,
    Optional,
    Callable,
    Type,
    Iterator,
    List,
    Sequence,
)
from http.client import HTTPConnection
from urllib.parse import urlparse

from ..pipeline import (
    PipelineRequest,
    PipelineResponse,
    PipelineContext,
)
from ..pipeline._tools import await_result as _await_result

if TYPE_CHECKING:
    # importing both the py3 RestHttpRequest and the fallback RestHttpRequest
    from azure.core.rest._rest_py3 import HttpRequest as RestHttpRequestPy3
    from azure.core.pipeline.transport import (
        HttpRequest as PipelineTransportHttpRequest,
    )

    HTTPRequestType = Union[RestHttpRequestPy3, PipelineTransportHttpRequest]
    from ..pipeline.policies import SansIOHTTPPolicy
    from azure.core.pipeline.transport import (  # pylint: disable=non-abstract-transport-import
        HttpResponse as PipelineTransportHttpResponse,
        AioHttpTransportResponse as PipelineTransportAioHttpTransportResponse,
    )
    from azure.core.pipeline.transport._base import (
        _HttpResponseBase as PipelineTransportHttpResponseBase,
    )
    from azure.core.rest._helpers import FilesType, FileType, FileContent

binary_type = str


class BytesIOSocket:
    """Mocking the "makefile" of socket for HTTPResponse.
    This can be used to create a http.client.HTTPResponse object
    based on bytes and not a real socket.

    :param bytes bytes_data: The bytes to use to mock the socket.
    """

    def __init__(self, bytes_data):
        self.bytes_data = bytes_data

    def makefile(self, *_):
        return BytesIO(self.bytes_data)


def _format_parameters_helper(http_request, params):
    """Helper for format_parameters.

    Format parameters into a valid query string.
    It's assumed all parameters have already been quoted as
    valid URL strings.

    :param http_request: The http request whose parameters
     we are trying to format
    :type http_request: any
    :param dict params: A dictionary of parameters.
    """
    query = urlparse(http_request.url).query
    if query:
        http_request.url = http_request.url.partition("?")[0]
        existing_params = {p[0]: p[-1] for p in [p.partition("=") for p in query.split("&")]}
        params.update(existing_params)
    query_params = []
    for k, v in params.items():
        if isinstance(v, list):
            for w in v:
                if w is None:
                    raise ValueError("Query parameter {} cannot be None".format(k))
                query_params.append("{}={}".format(k, w))
        else:
            if v is None:
                raise ValueError("Query parameter {} cannot be None".format(k))
            query_params.append("{}={}".format(k, v))
    query = "?" + "&".join(query_params)
    http_request.url = http_request.url + query


def _pad_attr_name(attr: str, backcompat_attrs: Sequence[str]) -> str:
    """Pad hidden attributes so users can access them.

    Currently, for our backcompat attributes, we define them
    as private, so they're hidden from intellisense and sphinx,
    but still allow users to access them as public attributes
    for backcompat purposes. This function is called so if
    users access publicly call a private backcompat attribute,
    we can return them the private variable in getattr

    :param str attr: The attribute name
    :param list[str] backcompat_attrs: The list of backcompat attributes
    :rtype: str
    :return: The padded attribute name
    """
    return "_{}".format(attr) if attr in backcompat_attrs else attr


def _prepare_multipart_body_helper(http_request: "HTTPRequestType", content_index: int = 0) -> int:
    """Helper for prepare_multipart_body.

    Will prepare the body of this request according to the multipart information.

    This call assumes the on_request policies have been applied already in their
    correct context (sync/async)

    Does nothing if "set_multipart_mixed" was never called.
    :param http_request: The http request whose multipart body we are trying
     to prepare
    :type http_request: any
    :param int content_index: The current index of parts within the batch message.
    :returns: The updated index after all parts in this request have been added.
    :rtype: int
    """
    if not http_request.multipart_mixed_info:
        return 0

    requests: Sequence["HTTPRequestType"] = http_request.multipart_mixed_info[0]
    boundary: Optional[str] = http_request.multipart_mixed_info[2]

    # Update the main request with the body
    main_message = Message()
    main_message.add_header("Content-Type", "multipart/mixed")
    if boundary:
        main_message.set_boundary(boundary)

    for req in requests:
        part_message = Message()
        if req.multipart_mixed_info:
            content_index = req.prepare_multipart_body(content_index=content_index)
            part_message.add_header("Content-Type", req.headers["Content-Type"])
            payload = req.serialize()
            # We need to remove the ~HTTP/1.1 prefix along with the added content-length
            payload = payload[payload.index(b"--") :]
        else:
            part_message.add_header("Content-Type", "application/http")
            part_message.add_header("Content-Transfer-Encoding", "binary")
            part_message.add_header("Content-ID", str(content_index))
            payload = req.serialize()
            content_index += 1
        part_message.set_payload(payload)
        main_message.attach(part_message)

    full_message = main_message.as_bytes(policy=HTTP)
    # From "as_bytes" doc:
    #  Flattening the message may trigger changes to the EmailMessage if defaults need to be filled in to complete
    #  the transformation to a string (for example, MIME boundaries may be generated or modified).
    # After this call, we know `get_boundary` will return a valid boundary and not None. Mypy doesn't know that.
    final_boundary: str = cast(str, main_message.get_boundary())
    eol = b"\r\n"
    _, _, body = full_message.split(eol, 2)
    http_request.set_bytes_body(body)
    http_request.headers["Content-Type"] = "multipart/mixed; boundary=" + final_boundary
    return content_index


class _HTTPSerializer(HTTPConnection):
    """Hacking the stdlib HTTPConnection to serialize HTTP request as strings."""

    def __init__(self, *args, **kwargs):
        self.buffer = b""
        kwargs.setdefault("host", "fakehost")
        super(_HTTPSerializer, self).__init__(*args, **kwargs)

    def putheader(self, header, *values):
        if header in ["Host", "Accept-Encoding"]:
            return
        super(_HTTPSerializer, self).putheader(header, *values)

    def send(self, data):
        self.buffer += data


def _serialize_request(http_request: "HTTPRequestType") -> bytes:
    """Helper for serialize.

    Serialize a request using the application/http spec/

    :param http_request: The http request which we are trying
     to serialize.
    :type http_request: any
    :rtype: bytes
    :return: The serialized request
    """
    if isinstance(http_request.body, dict):
        raise TypeError("Cannot serialize an HTTPRequest with dict body.")
    serializer = _HTTPSerializer()
    serializer.request(
        method=http_request.method,
        url=http_request.url,
        body=http_request.body,
        headers=http_request.headers,
    )
    return serializer.buffer


def _decode_parts_helper(
    response: "PipelineTransportHttpResponseBase",
    message: Message,
    http_response_type: Type["PipelineTransportHttpResponseBase"],
    requests: Sequence["PipelineTransportHttpRequest"],
    deserialize_response: Callable,
) -> List["PipelineTransportHttpResponse"]:
    """Helper for _decode_parts.

    Rebuild an HTTP response from pure string.

    :param response: The response to decode
    :type response: ~azure.core.pipeline.transport.HttpResponse
    :param message: The message to decode
    :type message: ~email.message.Message
    :param http_response_type: The type of response to return
    :type http_response_type: ~azure.core.pipeline.transport.HttpResponse
    :param requests: The requests that were batched together
    :type requests: list[~azure.core.pipeline.transport.HttpRequest]
    :param deserialize_response: The function to deserialize the response
    :type deserialize_response: callable
    :rtype: list[~azure.core.pipeline.transport.HttpResponse]
    :return: The list of responses
    """
    responses = []
    for index, raw_response in enumerate(message.get_payload()):
        content_type = raw_response.get_content_type()
        if content_type == "application/http":
            try:
                matching_request = requests[index]
            except IndexError:
                # If we have no matching request, this could mean that we had an empty batch.
                # The request object is only needed to get the HTTP METHOD and to store in the response object,
                # so let's just use the parent request so allow the rest of the deserialization to continue.
                matching_request = response.request
            responses.append(
                deserialize_response(
                    raw_response.get_payload(decode=True),
                    matching_request,
                    http_response_type=http_response_type,
                )
            )
        elif content_type == "multipart/mixed" and requests[index].multipart_mixed_info:
            # The message batch contains one or more change sets
            changeset_requests = requests[index].multipart_mixed_info[0]  # type: ignore
            changeset_responses = response._decode_parts(  # pylint: disable=protected-access
                raw_response, http_response_type, changeset_requests
            )
            responses.extend(changeset_responses)
        else:
            raise ValueError("Multipart doesn't support part other than application/http for now")
    return responses


def _get_raw_parts_helper(response, http_response_type: Type):
    """Helper for _get_raw_parts

    Assuming this body is multipart, return the iterator or parts.

    If parts are application/http use http_response_type or HttpClientTransportResponse
    as envelope.

    :param response: The response to decode
    :type response: ~azure.core.pipeline.transport.HttpResponse
    :param http_response_type: The type of response to return
    :type http_response_type: any
    :rtype: iterator[~azure.core.pipeline.transport.HttpResponse]
    :return: The parts of the response
    """
    body_as_bytes = response.body()
    # In order to use email.message parser, I need full HTTP bytes. Faking something to make the parser happy
    http_body = b"Content-Type: " + response.content_type.encode("ascii") + b"\r\n\r\n" + body_as_bytes
    message: Message = message_parser(http_body)
    requests = response.request.multipart_mixed_info[0]
    return response._decode_parts(message, http_response_type, requests)  # pylint: disable=protected-access


def _parts_helper(
    response: "PipelineTransportHttpResponse",
) -> Iterator["PipelineTransportHttpResponse"]:
    """Assuming the content-type is multipart/mixed, will return the parts as an iterator.

    :param response: The response to decode
    :type response: ~azure.core.pipeline.transport.HttpResponse
    :rtype: iterator[HttpResponse]
    :return: The parts of the response
    :raises ValueError: If the content is not multipart/mixed
    """
    if not response.content_type or not response.content_type.startswith("multipart/mixed"):
        raise ValueError("You can't get parts if the response is not multipart/mixed")

    responses = response._get_raw_parts()  # pylint: disable=protected-access
    if response.request.multipart_mixed_info:
        policies: Sequence["SansIOHTTPPolicy"] = response.request.multipart_mixed_info[1]

        # Apply on_response concurrently to all requests
        import concurrent.futures

        def parse_responses(response):
            http_request = response.request
            context = PipelineContext(None)
            pipeline_request = PipelineRequest(http_request, context)
            pipeline_response = PipelineResponse(http_request, response, context=context)

            for policy in policies:
                _await_result(policy.on_response, pipeline_request, pipeline_response)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # List comprehension to raise exceptions if happened
            [  # pylint: disable=expression-not-assigned, unnecessary-comprehension
                _ for _ in executor.map(parse_responses, responses)
            ]

    return responses


def _format_data_helper(data: "FileType") -> Union[Tuple[Optional[str], str], Tuple[Optional[str], "FileContent", str]]:
    """Helper for _format_data.

    Format field data according to whether it is a stream or
    a string for a form-data request.

    :param data: The request field data.
    :type data: str or file-like object.
    :rtype: tuple[str, IO, str] or tuple[None, str]
    :return: A tuple of (data name, data IO, "application/octet-stream") or (None, data str)
    """
    content_type: Optional[str] = None
    filename: Optional[str] = None
    if isinstance(data, tuple):
        if len(data) == 2:
            # Filename and file bytes are included
            filename, file_bytes = cast(Tuple[Optional[str], "FileContent"], data)
        elif len(data) == 3:
            # Filename, file object, and content_type are included
            filename, file_bytes, content_type = cast(Tuple[Optional[str], "FileContent", str], data)
        else:
            raise ValueError(
                "Unexpected data format. Expected file, or tuple of (filename, file_bytes) or "
                "(filename, file_bytes, content_type)."
            )
    else:
        # here we just get the file content
        if hasattr(data, "read"):
            data = cast(IO, data)
            try:
                if data.name[0] != "<" and data.name[-1] != ">":
                    filename = os.path.basename(data.name)
            except (AttributeError, TypeError):
                pass
            content_type = "application/octet-stream"
        file_bytes = data
    if content_type:
        return (filename, file_bytes, content_type)
    return (filename, cast(str, file_bytes))


def _aiohttp_body_helper(
    response: "PipelineTransportAioHttpTransportResponse",
) -> bytes:
    # pylint: disable=protected-access
    """Helper for body method of Aiohttp responses.

    Since aiohttp body methods need decompression work synchronously,
    need to share this code across old and new aiohttp transport responses
    for backcompat.

    :param response: The response to decode
    :type response: ~azure.core.pipeline.transport.AioHttpTransportResponse
    :rtype: bytes
    :return: The response's bytes
    """
    if response._content is None:
        raise ValueError("Body is not available. Call async method load_body, or do your call with stream=False.")
    if not response._decompress:
        return response._content
    if response._decompressed_content:
        return response._content
    enc = response.headers.get("Content-Encoding")
    if not enc:
        return response._content
    enc = enc.lower()
    if enc in ("gzip", "deflate"):
        import zlib

        zlib_mode = (16 + zlib.MAX_WBITS) if enc == "gzip" else -zlib.MAX_WBITS
        decompressor = zlib.decompressobj(wbits=zlib_mode)
        response._content = decompressor.decompress(response._content)
        response._decompressed_content = True
        return response._content
    return response._content


def get_file_items(files: "FilesType") -> Sequence[Tuple[str, "FileType"]]:
    if isinstance(files, Mapping):
        # casting because ItemsView technically isn't a Sequence, even
        # though realistically it is ordered python 3.7 and after
        return cast(Sequence[Tuple[str, "FileType"]], files.items())
    return files
