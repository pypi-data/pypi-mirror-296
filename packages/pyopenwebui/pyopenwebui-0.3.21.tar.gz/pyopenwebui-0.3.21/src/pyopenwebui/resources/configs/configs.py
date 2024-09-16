# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import config_import_params
from .banners import (
    BannersResource,
    AsyncBannersResource,
    BannersResourceWithRawResponse,
    AsyncBannersResourceWithRawResponse,
    BannersResourceWithStreamingResponse,
    AsyncBannersResourceWithStreamingResponse,
)
from .default import (
    DefaultResource,
    AsyncDefaultResource,
    DefaultResourceWithRawResponse,
    AsyncDefaultResourceWithRawResponse,
    DefaultResourceWithStreamingResponse,
    AsyncDefaultResourceWithStreamingResponse,
)
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
from ..._base_client import make_request_options
from .default.default import DefaultResource, AsyncDefaultResource

__all__ = ["ConfigsResource", "AsyncConfigsResource"]


class ConfigsResource(SyncAPIResource):
    @cached_property
    def default(self) -> DefaultResource:
        return DefaultResource(self._client)

    @cached_property
    def banners(self) -> BannersResource:
        return BannersResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return ConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return ConfigsResourceWithStreamingResponse(self)

    def export(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Export Config"""
        return self._get(
            "/configs/export",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def import_(
        self,
        *,
        config: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Import Config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/configs/import",
            body=maybe_transform({"config": config}, config_import_params.ConfigImportParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncConfigsResource(AsyncAPIResource):
    @cached_property
    def default(self) -> AsyncDefaultResource:
        return AsyncDefaultResource(self._client)

    @cached_property
    def banners(self) -> AsyncBannersResource:
        return AsyncBannersResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncConfigsResourceWithStreamingResponse(self)

    async def export(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Export Config"""
        return await self._get(
            "/configs/export",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def import_(
        self,
        *,
        config: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Import Config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/configs/import",
            body=await async_maybe_transform({"config": config}, config_import_params.ConfigImportParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ConfigsResourceWithRawResponse:
    def __init__(self, configs: ConfigsResource) -> None:
        self._configs = configs

        self.export = to_raw_response_wrapper(
            configs.export,
        )
        self.import_ = to_raw_response_wrapper(
            configs.import_,
        )

    @cached_property
    def default(self) -> DefaultResourceWithRawResponse:
        return DefaultResourceWithRawResponse(self._configs.default)

    @cached_property
    def banners(self) -> BannersResourceWithRawResponse:
        return BannersResourceWithRawResponse(self._configs.banners)


class AsyncConfigsResourceWithRawResponse:
    def __init__(self, configs: AsyncConfigsResource) -> None:
        self._configs = configs

        self.export = async_to_raw_response_wrapper(
            configs.export,
        )
        self.import_ = async_to_raw_response_wrapper(
            configs.import_,
        )

    @cached_property
    def default(self) -> AsyncDefaultResourceWithRawResponse:
        return AsyncDefaultResourceWithRawResponse(self._configs.default)

    @cached_property
    def banners(self) -> AsyncBannersResourceWithRawResponse:
        return AsyncBannersResourceWithRawResponse(self._configs.banners)


class ConfigsResourceWithStreamingResponse:
    def __init__(self, configs: ConfigsResource) -> None:
        self._configs = configs

        self.export = to_streamed_response_wrapper(
            configs.export,
        )
        self.import_ = to_streamed_response_wrapper(
            configs.import_,
        )

    @cached_property
    def default(self) -> DefaultResourceWithStreamingResponse:
        return DefaultResourceWithStreamingResponse(self._configs.default)

    @cached_property
    def banners(self) -> BannersResourceWithStreamingResponse:
        return BannersResourceWithStreamingResponse(self._configs.banners)


class AsyncConfigsResourceWithStreamingResponse:
    def __init__(self, configs: AsyncConfigsResource) -> None:
        self._configs = configs

        self.export = async_to_streamed_response_wrapper(
            configs.export,
        )
        self.import_ = async_to_streamed_response_wrapper(
            configs.import_,
        )

    @cached_property
    def default(self) -> AsyncDefaultResourceWithStreamingResponse:
        return AsyncDefaultResourceWithStreamingResponse(self._configs.default)

    @cached_property
    def banners(self) -> AsyncBannersResourceWithStreamingResponse:
        return AsyncBannersResourceWithStreamingResponse(self._configs.banners)
