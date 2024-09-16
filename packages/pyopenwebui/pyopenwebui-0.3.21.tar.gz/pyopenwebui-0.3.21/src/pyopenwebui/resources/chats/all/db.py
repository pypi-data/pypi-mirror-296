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
from ....types.chats.all.db_list_response import DBListResponse

__all__ = ["DBResource", "AsyncDBResource"]


class DBResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DBResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return DBResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DBResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return DBResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DBListResponse:
        """Get All User Chats In Db"""
        return self._get(
            "/chats/all/db",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DBListResponse,
        )


class AsyncDBResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDBResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDBResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDBResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncDBResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DBListResponse:
        """Get All User Chats In Db"""
        return await self._get(
            "/chats/all/db",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DBListResponse,
        )


class DBResourceWithRawResponse:
    def __init__(self, db: DBResource) -> None:
        self._db = db

        self.list = to_raw_response_wrapper(
            db.list,
        )


class AsyncDBResourceWithRawResponse:
    def __init__(self, db: AsyncDBResource) -> None:
        self._db = db

        self.list = async_to_raw_response_wrapper(
            db.list,
        )


class DBResourceWithStreamingResponse:
    def __init__(self, db: DBResource) -> None:
        self._db = db

        self.list = to_streamed_response_wrapper(
            db.list,
        )


class AsyncDBResourceWithStreamingResponse:
    def __init__(self, db: AsyncDBResource) -> None:
        self._db = db

        self.list = async_to_streamed_response_wrapper(
            db.list,
        )
