# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

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
from ...types.utils import pdf_create_params
from ..._base_client import make_request_options

__all__ = ["PdfResource", "AsyncPdfResource"]


class PdfResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PdfResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return PdfResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PdfResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return PdfResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        messages: Iterable[object],
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Download Chat As Pdf

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/utils/pdf",
            body=maybe_transform(
                {
                    "messages": messages,
                    "title": title,
                },
                pdf_create_params.PdfCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncPdfResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPdfResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPdfResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPdfResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncPdfResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        messages: Iterable[object],
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Download Chat As Pdf

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/utils/pdf",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "title": title,
                },
                pdf_create_params.PdfCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class PdfResourceWithRawResponse:
    def __init__(self, pdf: PdfResource) -> None:
        self._pdf = pdf

        self.create = to_raw_response_wrapper(
            pdf.create,
        )


class AsyncPdfResourceWithRawResponse:
    def __init__(self, pdf: AsyncPdfResource) -> None:
        self._pdf = pdf

        self.create = async_to_raw_response_wrapper(
            pdf.create,
        )


class PdfResourceWithStreamingResponse:
    def __init__(self, pdf: PdfResource) -> None:
        self._pdf = pdf

        self.create = to_streamed_response_wrapper(
            pdf.create,
        )


class AsyncPdfResourceWithStreamingResponse:
    def __init__(self, pdf: AsyncPdfResource) -> None:
        self._pdf = pdf

        self.create = async_to_streamed_response_wrapper(
            pdf.create,
        )
