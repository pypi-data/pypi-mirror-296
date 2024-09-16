# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .spec import (
    SpecResource,
    AsyncSpecResource,
    SpecResourceWithRawResponse,
    AsyncSpecResourceWithRawResponse,
    SpecResourceWithStreamingResponse,
    AsyncSpecResourceWithStreamingResponse,
)
from .user import (
    UserResource,
    AsyncUserResource,
    UserResourceWithRawResponse,
    AsyncUserResourceWithRawResponse,
    UserResourceWithStreamingResponse,
    AsyncUserResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .user.user import UserResource, AsyncUserResource
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....types.tools import valve_update_params
from ...._base_client import make_request_options

__all__ = ["ValvesResource", "AsyncValvesResource"]


class ValvesResource(SyncAPIResource):
    @cached_property
    def spec(self) -> SpecResource:
        return SpecResource(self._client)

    @cached_property
    def user(self) -> UserResource:
        return UserResource(self._client)

    @cached_property
    def with_raw_response(self) -> ValvesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return ValvesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValvesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return ValvesResourceWithStreamingResponse(self)

    def update(
        self,
        id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Update Toolkit Valves By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/tools/id/{id}/valves/update",
            body=maybe_transform(body, valve_update_params.ValveUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncValvesResource(AsyncAPIResource):
    @cached_property
    def spec(self) -> AsyncSpecResource:
        return AsyncSpecResource(self._client)

    @cached_property
    def user(self) -> AsyncUserResource:
        return AsyncUserResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncValvesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncValvesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValvesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncValvesResourceWithStreamingResponse(self)

    async def update(
        self,
        id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Update Toolkit Valves By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/tools/id/{id}/valves/update",
            body=await async_maybe_transform(body, valve_update_params.ValveUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ValvesResourceWithRawResponse:
    def __init__(self, valves: ValvesResource) -> None:
        self._valves = valves

        self.update = to_raw_response_wrapper(
            valves.update,
        )

    @cached_property
    def spec(self) -> SpecResourceWithRawResponse:
        return SpecResourceWithRawResponse(self._valves.spec)

    @cached_property
    def user(self) -> UserResourceWithRawResponse:
        return UserResourceWithRawResponse(self._valves.user)


class AsyncValvesResourceWithRawResponse:
    def __init__(self, valves: AsyncValvesResource) -> None:
        self._valves = valves

        self.update = async_to_raw_response_wrapper(
            valves.update,
        )

    @cached_property
    def spec(self) -> AsyncSpecResourceWithRawResponse:
        return AsyncSpecResourceWithRawResponse(self._valves.spec)

    @cached_property
    def user(self) -> AsyncUserResourceWithRawResponse:
        return AsyncUserResourceWithRawResponse(self._valves.user)


class ValvesResourceWithStreamingResponse:
    def __init__(self, valves: ValvesResource) -> None:
        self._valves = valves

        self.update = to_streamed_response_wrapper(
            valves.update,
        )

    @cached_property
    def spec(self) -> SpecResourceWithStreamingResponse:
        return SpecResourceWithStreamingResponse(self._valves.spec)

    @cached_property
    def user(self) -> UserResourceWithStreamingResponse:
        return UserResourceWithStreamingResponse(self._valves.user)


class AsyncValvesResourceWithStreamingResponse:
    def __init__(self, valves: AsyncValvesResource) -> None:
        self._valves = valves

        self.update = async_to_streamed_response_wrapper(
            valves.update,
        )

    @cached_property
    def spec(self) -> AsyncSpecResourceWithStreamingResponse:
        return AsyncSpecResourceWithStreamingResponse(self._valves.spec)

    @cached_property
    def user(self) -> AsyncUserResourceWithStreamingResponse:
        return AsyncUserResourceWithStreamingResponse(self._valves.user)
