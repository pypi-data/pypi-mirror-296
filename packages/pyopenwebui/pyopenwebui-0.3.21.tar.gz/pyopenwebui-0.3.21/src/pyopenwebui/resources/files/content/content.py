# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .file_name import (
    FileNameResource,
    AsyncFileNameResource,
    FileNameResourceWithRawResponse,
    AsyncFileNameResourceWithRawResponse,
    FileNameResourceWithStreamingResponse,
    AsyncFileNameResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.shared.file_model import FileModel

__all__ = ["ContentResource", "AsyncContentResource"]


class ContentResource(SyncAPIResource):
    @cached_property
    def file_name(self) -> FileNameResource:
        return FileNameResource(self._client)

    @cached_property
    def with_raw_response(self) -> ContentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return ContentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ContentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return ContentResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FileModel]:
        """
        Get File Content By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/files/{id}/content",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileModel,
        )


class AsyncContentResource(AsyncAPIResource):
    @cached_property
    def file_name(self) -> AsyncFileNameResource:
        return AsyncFileNameResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncContentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncContentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncContentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncContentResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FileModel]:
        """
        Get File Content By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/files/{id}/content",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileModel,
        )


class ContentResourceWithRawResponse:
    def __init__(self, content: ContentResource) -> None:
        self._content = content

        self.retrieve = to_raw_response_wrapper(
            content.retrieve,
        )

    @cached_property
    def file_name(self) -> FileNameResourceWithRawResponse:
        return FileNameResourceWithRawResponse(self._content.file_name)


class AsyncContentResourceWithRawResponse:
    def __init__(self, content: AsyncContentResource) -> None:
        self._content = content

        self.retrieve = async_to_raw_response_wrapper(
            content.retrieve,
        )

    @cached_property
    def file_name(self) -> AsyncFileNameResourceWithRawResponse:
        return AsyncFileNameResourceWithRawResponse(self._content.file_name)


class ContentResourceWithStreamingResponse:
    def __init__(self, content: ContentResource) -> None:
        self._content = content

        self.retrieve = to_streamed_response_wrapper(
            content.retrieve,
        )

    @cached_property
    def file_name(self) -> FileNameResourceWithStreamingResponse:
        return FileNameResourceWithStreamingResponse(self._content.file_name)


class AsyncContentResourceWithStreamingResponse:
    def __init__(self, content: AsyncContentResource) -> None:
        self._content = content

        self.retrieve = async_to_streamed_response_wrapper(
            content.retrieve,
        )

    @cached_property
    def file_name(self) -> AsyncFileNameResourceWithStreamingResponse:
        return AsyncFileNameResourceWithStreamingResponse(self._content.file_name)
