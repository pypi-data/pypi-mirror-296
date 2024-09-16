# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .tags import (
    TagsResource,
    AsyncTagsResource,
    TagsResourceWithRawResponse,
    AsyncTagsResourceWithRawResponse,
    TagsResourceWithStreamingResponse,
    AsyncTagsResourceWithStreamingResponse,
)
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
from ....types.documents import doc_delete_params, doc_update_params, doc_retrieve_params
from ....types.shared.document_response import DocumentResponse
from ....types.documents.doc_delete_response import DocDeleteResponse

__all__ = ["DocResource", "AsyncDocResource"]


class DocResource(SyncAPIResource):
    @cached_property
    def tags(self) -> TagsResource:
        return TagsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DocResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return DocResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return DocResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[DocumentResponse]:
        """
        Get Doc By Name

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/documents/doc",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"name": name}, doc_retrieve_params.DocRetrieveParams),
            ),
            cast_to=DocumentResponse,
        )

    def update(
        self,
        *,
        query_name: str,
        body_name: str,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[DocumentResponse]:
        """
        Update Doc By Name

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/documents/doc/update",
            body=maybe_transform(
                {
                    "name": body_name,
                    "title": title,
                },
                doc_update_params.DocUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"name": query_name}, doc_update_params.DocUpdateParams),
            ),
            cast_to=DocumentResponse,
        )

    def delete(
        self,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocDeleteResponse:
        """
        Delete Doc By Name

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            "/documents/doc/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"name": name}, doc_delete_params.DocDeleteParams),
            ),
            cast_to=DocDeleteResponse,
        )


class AsyncDocResource(AsyncAPIResource):
    @cached_property
    def tags(self) -> AsyncTagsResource:
        return AsyncTagsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDocResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDocResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncDocResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[DocumentResponse]:
        """
        Get Doc By Name

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/documents/doc",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"name": name}, doc_retrieve_params.DocRetrieveParams),
            ),
            cast_to=DocumentResponse,
        )

    async def update(
        self,
        *,
        query_name: str,
        body_name: str,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[DocumentResponse]:
        """
        Update Doc By Name

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/documents/doc/update",
            body=await async_maybe_transform(
                {
                    "name": body_name,
                    "title": title,
                },
                doc_update_params.DocUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"name": query_name}, doc_update_params.DocUpdateParams),
            ),
            cast_to=DocumentResponse,
        )

    async def delete(
        self,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocDeleteResponse:
        """
        Delete Doc By Name

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            "/documents/doc/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"name": name}, doc_delete_params.DocDeleteParams),
            ),
            cast_to=DocDeleteResponse,
        )


class DocResourceWithRawResponse:
    def __init__(self, doc: DocResource) -> None:
        self._doc = doc

        self.retrieve = to_raw_response_wrapper(
            doc.retrieve,
        )
        self.update = to_raw_response_wrapper(
            doc.update,
        )
        self.delete = to_raw_response_wrapper(
            doc.delete,
        )

    @cached_property
    def tags(self) -> TagsResourceWithRawResponse:
        return TagsResourceWithRawResponse(self._doc.tags)


class AsyncDocResourceWithRawResponse:
    def __init__(self, doc: AsyncDocResource) -> None:
        self._doc = doc

        self.retrieve = async_to_raw_response_wrapper(
            doc.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            doc.update,
        )
        self.delete = async_to_raw_response_wrapper(
            doc.delete,
        )

    @cached_property
    def tags(self) -> AsyncTagsResourceWithRawResponse:
        return AsyncTagsResourceWithRawResponse(self._doc.tags)


class DocResourceWithStreamingResponse:
    def __init__(self, doc: DocResource) -> None:
        self._doc = doc

        self.retrieve = to_streamed_response_wrapper(
            doc.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            doc.update,
        )
        self.delete = to_streamed_response_wrapper(
            doc.delete,
        )

    @cached_property
    def tags(self) -> TagsResourceWithStreamingResponse:
        return TagsResourceWithStreamingResponse(self._doc.tags)


class AsyncDocResourceWithStreamingResponse:
    def __init__(self, doc: AsyncDocResource) -> None:
        self._doc = doc

        self.retrieve = async_to_streamed_response_wrapper(
            doc.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            doc.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            doc.delete,
        )

    @cached_property
    def tags(self) -> AsyncTagsResourceWithStreamingResponse:
        return AsyncTagsResourceWithStreamingResponse(self._doc.tags)
