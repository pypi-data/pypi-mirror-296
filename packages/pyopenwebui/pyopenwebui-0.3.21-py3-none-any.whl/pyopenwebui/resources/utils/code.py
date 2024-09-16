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
from ...types.utils import code_format_params
from ..._base_client import make_request_options

__all__ = ["CodeResource", "AsyncCodeResource"]


class CodeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CodeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return CodeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CodeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return CodeResourceWithStreamingResponse(self)

    def format(
        self,
        *,
        code: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Format Code

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/utils/code/format",
            body=maybe_transform({"code": code}, code_format_params.CodeFormatParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncCodeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCodeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCodeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCodeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncCodeResourceWithStreamingResponse(self)

    async def format(
        self,
        *,
        code: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Format Code

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/utils/code/format",
            body=await async_maybe_transform({"code": code}, code_format_params.CodeFormatParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class CodeResourceWithRawResponse:
    def __init__(self, code: CodeResource) -> None:
        self._code = code

        self.format = to_raw_response_wrapper(
            code.format,
        )


class AsyncCodeResourceWithRawResponse:
    def __init__(self, code: AsyncCodeResource) -> None:
        self._code = code

        self.format = async_to_raw_response_wrapper(
            code.format,
        )


class CodeResourceWithStreamingResponse:
    def __init__(self, code: CodeResource) -> None:
        self._code = code

        self.format = to_streamed_response_wrapper(
            code.format,
        )


class AsyncCodeResourceWithStreamingResponse:
    def __init__(self, code: AsyncCodeResource) -> None:
        self._code = code

        self.format = async_to_streamed_response_wrapper(
            code.format,
        )
