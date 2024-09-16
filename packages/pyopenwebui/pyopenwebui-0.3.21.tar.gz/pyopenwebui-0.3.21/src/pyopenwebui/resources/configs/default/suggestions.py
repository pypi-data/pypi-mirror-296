# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
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
from ....types.configs.default import suggestion_create_params
from ....types.configs.default.prompt_suggestion_param import PromptSuggestionParam
from ....types.configs.default.suggestion_create_response import SuggestionCreateResponse

__all__ = ["SuggestionsResource", "AsyncSuggestionsResource"]


class SuggestionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SuggestionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return SuggestionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SuggestionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return SuggestionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        suggestions: Iterable[PromptSuggestionParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SuggestionCreateResponse:
        """
        Set Global Default Suggestions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/configs/default/suggestions",
            body=maybe_transform({"suggestions": suggestions}, suggestion_create_params.SuggestionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SuggestionCreateResponse,
        )


class AsyncSuggestionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSuggestionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSuggestionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSuggestionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncSuggestionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        suggestions: Iterable[PromptSuggestionParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SuggestionCreateResponse:
        """
        Set Global Default Suggestions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/configs/default/suggestions",
            body=await async_maybe_transform(
                {"suggestions": suggestions}, suggestion_create_params.SuggestionCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SuggestionCreateResponse,
        )


class SuggestionsResourceWithRawResponse:
    def __init__(self, suggestions: SuggestionsResource) -> None:
        self._suggestions = suggestions

        self.create = to_raw_response_wrapper(
            suggestions.create,
        )


class AsyncSuggestionsResourceWithRawResponse:
    def __init__(self, suggestions: AsyncSuggestionsResource) -> None:
        self._suggestions = suggestions

        self.create = async_to_raw_response_wrapper(
            suggestions.create,
        )


class SuggestionsResourceWithStreamingResponse:
    def __init__(self, suggestions: SuggestionsResource) -> None:
        self._suggestions = suggestions

        self.create = to_streamed_response_wrapper(
            suggestions.create,
        )


class AsyncSuggestionsResourceWithStreamingResponse:
    def __init__(self, suggestions: AsyncSuggestionsResource) -> None:
        self._suggestions = suggestions

        self.create = async_to_streamed_response_wrapper(
            suggestions.create,
        )
