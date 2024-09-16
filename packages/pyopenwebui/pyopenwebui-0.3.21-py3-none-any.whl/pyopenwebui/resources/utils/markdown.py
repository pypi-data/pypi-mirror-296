# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.utils import markdown_create_params
from ..._base_client import make_request_options

__all__ = ["MarkdownResource", "AsyncMarkdownResource"]


class MarkdownResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MarkdownResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return MarkdownResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MarkdownResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return MarkdownResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        md: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get Html From Markdown

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/utils/markdown",
            body=maybe_transform({"md": md}, markdown_create_params.MarkdownCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncMarkdownResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMarkdownResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMarkdownResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMarkdownResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncMarkdownResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        md: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get Html From Markdown

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/utils/markdown",
            body=await async_maybe_transform({"md": md}, markdown_create_params.MarkdownCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class MarkdownResourceWithRawResponse:
    def __init__(self, markdown: MarkdownResource) -> None:
        self._markdown = markdown

        self.create = to_raw_response_wrapper(
            markdown.create,
        )


class AsyncMarkdownResourceWithRawResponse:
    def __init__(self, markdown: AsyncMarkdownResource) -> None:
        self._markdown = markdown

        self.create = async_to_raw_response_wrapper(
            markdown.create,
        )


class MarkdownResourceWithStreamingResponse:
    def __init__(self, markdown: MarkdownResource) -> None:
        self._markdown = markdown

        self.create = to_streamed_response_wrapper(
            markdown.create,
        )


class AsyncMarkdownResourceWithStreamingResponse:
    def __init__(self, markdown: AsyncMarkdownResource) -> None:
        self._markdown = markdown

        self.create = async_to_streamed_response_wrapper(
            markdown.create,
        )
