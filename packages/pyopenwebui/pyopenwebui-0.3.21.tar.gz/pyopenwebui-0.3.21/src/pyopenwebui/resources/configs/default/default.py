# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .models import (
    ModelsResource,
    AsyncModelsResource,
    ModelsResourceWithRawResponse,
    AsyncModelsResourceWithRawResponse,
    ModelsResourceWithStreamingResponse,
    AsyncModelsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from .suggestions import (
    SuggestionsResource,
    AsyncSuggestionsResource,
    SuggestionsResourceWithRawResponse,
    AsyncSuggestionsResourceWithRawResponse,
    SuggestionsResourceWithStreamingResponse,
    AsyncSuggestionsResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["DefaultResource", "AsyncDefaultResource"]


class DefaultResource(SyncAPIResource):
    @cached_property
    def models(self) -> ModelsResource:
        return ModelsResource(self._client)

    @cached_property
    def suggestions(self) -> SuggestionsResource:
        return SuggestionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DefaultResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return DefaultResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DefaultResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return DefaultResourceWithStreamingResponse(self)


class AsyncDefaultResource(AsyncAPIResource):
    @cached_property
    def models(self) -> AsyncModelsResource:
        return AsyncModelsResource(self._client)

    @cached_property
    def suggestions(self) -> AsyncSuggestionsResource:
        return AsyncSuggestionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDefaultResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDefaultResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDefaultResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncDefaultResourceWithStreamingResponse(self)


class DefaultResourceWithRawResponse:
    def __init__(self, default: DefaultResource) -> None:
        self._default = default

    @cached_property
    def models(self) -> ModelsResourceWithRawResponse:
        return ModelsResourceWithRawResponse(self._default.models)

    @cached_property
    def suggestions(self) -> SuggestionsResourceWithRawResponse:
        return SuggestionsResourceWithRawResponse(self._default.suggestions)


class AsyncDefaultResourceWithRawResponse:
    def __init__(self, default: AsyncDefaultResource) -> None:
        self._default = default

    @cached_property
    def models(self) -> AsyncModelsResourceWithRawResponse:
        return AsyncModelsResourceWithRawResponse(self._default.models)

    @cached_property
    def suggestions(self) -> AsyncSuggestionsResourceWithRawResponse:
        return AsyncSuggestionsResourceWithRawResponse(self._default.suggestions)


class DefaultResourceWithStreamingResponse:
    def __init__(self, default: DefaultResource) -> None:
        self._default = default

    @cached_property
    def models(self) -> ModelsResourceWithStreamingResponse:
        return ModelsResourceWithStreamingResponse(self._default.models)

    @cached_property
    def suggestions(self) -> SuggestionsResourceWithStreamingResponse:
        return SuggestionsResourceWithStreamingResponse(self._default.suggestions)


class AsyncDefaultResourceWithStreamingResponse:
    def __init__(self, default: AsyncDefaultResource) -> None:
        self._default = default

    @cached_property
    def models(self) -> AsyncModelsResourceWithStreamingResponse:
        return AsyncModelsResourceWithStreamingResponse(self._default.models)

    @cached_property
    def suggestions(self) -> AsyncSuggestionsResourceWithStreamingResponse:
        return AsyncSuggestionsResourceWithStreamingResponse(self._default.suggestions)
