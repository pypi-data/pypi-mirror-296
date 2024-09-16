# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .config import (
    ConfigResource,
    AsyncConfigResource,
    ConfigResourceWithRawResponse,
    AsyncConfigResourceWithRawResponse,
    ConfigResourceWithStreamingResponse,
    AsyncConfigResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["LitellmResource", "AsyncLitellmResource"]


class LitellmResource(SyncAPIResource):
    @cached_property
    def config(self) -> ConfigResource:
        return ConfigResource(self._client)

    @cached_property
    def with_raw_response(self) -> LitellmResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return LitellmResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LitellmResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return LitellmResourceWithStreamingResponse(self)


class AsyncLitellmResource(AsyncAPIResource):
    @cached_property
    def config(self) -> AsyncConfigResource:
        return AsyncConfigResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncLitellmResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLitellmResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLitellmResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncLitellmResourceWithStreamingResponse(self)


class LitellmResourceWithRawResponse:
    def __init__(self, litellm: LitellmResource) -> None:
        self._litellm = litellm

    @cached_property
    def config(self) -> ConfigResourceWithRawResponse:
        return ConfigResourceWithRawResponse(self._litellm.config)


class AsyncLitellmResourceWithRawResponse:
    def __init__(self, litellm: AsyncLitellmResource) -> None:
        self._litellm = litellm

    @cached_property
    def config(self) -> AsyncConfigResourceWithRawResponse:
        return AsyncConfigResourceWithRawResponse(self._litellm.config)


class LitellmResourceWithStreamingResponse:
    def __init__(self, litellm: LitellmResource) -> None:
        self._litellm = litellm

    @cached_property
    def config(self) -> ConfigResourceWithStreamingResponse:
        return ConfigResourceWithStreamingResponse(self._litellm.config)


class AsyncLitellmResourceWithStreamingResponse:
    def __init__(self, litellm: AsyncLitellmResource) -> None:
        self._litellm = litellm

    @cached_property
    def config(self) -> AsyncConfigResourceWithStreamingResponse:
        return AsyncConfigResourceWithStreamingResponse(self._litellm.config)
