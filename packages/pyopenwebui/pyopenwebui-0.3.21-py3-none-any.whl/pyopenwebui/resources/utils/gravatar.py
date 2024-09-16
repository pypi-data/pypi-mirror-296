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
from ...types.utils import gravatar_retrieve_params
from ..._base_client import make_request_options

__all__ = ["GravatarResource", "AsyncGravatarResource"]


class GravatarResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GravatarResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return GravatarResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GravatarResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return GravatarResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        email: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get Gravatar

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/utils/gravatar",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"email": email}, gravatar_retrieve_params.GravatarRetrieveParams),
            ),
            cast_to=object,
        )


class AsyncGravatarResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGravatarResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGravatarResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGravatarResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncGravatarResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        email: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get Gravatar

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/utils/gravatar",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"email": email}, gravatar_retrieve_params.GravatarRetrieveParams),
            ),
            cast_to=object,
        )


class GravatarResourceWithRawResponse:
    def __init__(self, gravatar: GravatarResource) -> None:
        self._gravatar = gravatar

        self.retrieve = to_raw_response_wrapper(
            gravatar.retrieve,
        )


class AsyncGravatarResourceWithRawResponse:
    def __init__(self, gravatar: AsyncGravatarResource) -> None:
        self._gravatar = gravatar

        self.retrieve = async_to_raw_response_wrapper(
            gravatar.retrieve,
        )


class GravatarResourceWithStreamingResponse:
    def __init__(self, gravatar: GravatarResource) -> None:
        self._gravatar = gravatar

        self.retrieve = to_streamed_response_wrapper(
            gravatar.retrieve,
        )


class AsyncGravatarResourceWithStreamingResponse:
    def __init__(self, gravatar: AsyncGravatarResource) -> None:
        self._gravatar = gravatar

        self.retrieve = async_to_streamed_response_wrapper(
            gravatar.retrieve,
        )
