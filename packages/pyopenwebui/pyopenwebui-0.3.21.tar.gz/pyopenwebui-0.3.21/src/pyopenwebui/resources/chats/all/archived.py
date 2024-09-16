# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ....types.chats.all.archived_list_response import ArchivedListResponse

__all__ = ["ArchivedResource", "AsyncArchivedResource"]


class ArchivedResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ArchivedResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return ArchivedResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ArchivedResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return ArchivedResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArchivedListResponse:
        """Get User Archived Chats"""
        return self._get(
            "/chats/all/archived",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArchivedListResponse,
        )


class AsyncArchivedResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncArchivedResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncArchivedResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncArchivedResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncArchivedResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArchivedListResponse:
        """Get User Archived Chats"""
        return await self._get(
            "/chats/all/archived",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArchivedListResponse,
        )


class ArchivedResourceWithRawResponse:
    def __init__(self, archived: ArchivedResource) -> None:
        self._archived = archived

        self.list = to_raw_response_wrapper(
            archived.list,
        )


class AsyncArchivedResourceWithRawResponse:
    def __init__(self, archived: AsyncArchivedResource) -> None:
        self._archived = archived

        self.list = async_to_raw_response_wrapper(
            archived.list,
        )


class ArchivedResourceWithStreamingResponse:
    def __init__(self, archived: ArchivedResource) -> None:
        self._archived = archived

        self.list = to_streamed_response_wrapper(
            archived.list,
        )


class AsyncArchivedResourceWithStreamingResponse:
    def __init__(self, archived: AsyncArchivedResource) -> None:
        self._archived = archived

        self.list = async_to_streamed_response_wrapper(
            archived.list,
        )
