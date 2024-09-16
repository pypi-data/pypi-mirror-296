# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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

__all__ = ["FileNameResource", "AsyncFileNameResource"]


class FileNameResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FileNameResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return FileNameResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FileNameResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return FileNameResourceWithStreamingResponse(self)

    def retrieve(
        self,
        file_name: str,
        *,
        id: str,
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
        if not file_name:
            raise ValueError(f"Expected a non-empty value for `file_name` but received {file_name!r}")
        return self._get(
            f"/files/{id}/content/{file_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileModel,
        )


class AsyncFileNameResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFileNameResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFileNameResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFileNameResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncFileNameResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        file_name: str,
        *,
        id: str,
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
        if not file_name:
            raise ValueError(f"Expected a non-empty value for `file_name` but received {file_name!r}")
        return await self._get(
            f"/files/{id}/content/{file_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileModel,
        )


class FileNameResourceWithRawResponse:
    def __init__(self, file_name: FileNameResource) -> None:
        self._file_name = file_name

        self.retrieve = to_raw_response_wrapper(
            file_name.retrieve,
        )


class AsyncFileNameResourceWithRawResponse:
    def __init__(self, file_name: AsyncFileNameResource) -> None:
        self._file_name = file_name

        self.retrieve = async_to_raw_response_wrapper(
            file_name.retrieve,
        )


class FileNameResourceWithStreamingResponse:
    def __init__(self, file_name: FileNameResource) -> None:
        self._file_name = file_name

        self.retrieve = to_streamed_response_wrapper(
            file_name.retrieve,
        )


class AsyncFileNameResourceWithStreamingResponse:
    def __init__(self, file_name: AsyncFileNameResource) -> None:
        self._file_name = file_name

        self.retrieve = async_to_streamed_response_wrapper(
            file_name.retrieve,
        )
