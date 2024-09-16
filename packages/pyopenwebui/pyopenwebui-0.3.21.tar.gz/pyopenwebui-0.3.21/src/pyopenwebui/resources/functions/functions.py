# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .export import (
    ExportResource,
    AsyncExportResource,
    ExportResourceWithRawResponse,
    AsyncExportResourceWithRawResponse,
    ExportResourceWithStreamingResponse,
    AsyncExportResourceWithStreamingResponse,
)
from .valves import (
    ValvesResource,
    AsyncValvesResource,
    ValvesResourceWithRawResponse,
    AsyncValvesResourceWithRawResponse,
    ValvesResourceWithStreamingResponse,
    AsyncValvesResourceWithStreamingResponse,
)
from ...types import function_create_params, function_update_params
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
from .valves.valves import ValvesResource, AsyncValvesResource
from ..._base_client import make_request_options
from ...types.function_model import FunctionModel
from ...types.function_response import FunctionResponse
from ...types.function_list_response import FunctionListResponse
from ...types.function_delete_response import FunctionDeleteResponse

__all__ = ["FunctionsResource", "AsyncFunctionsResource"]


class FunctionsResource(SyncAPIResource):
    @cached_property
    def export(self) -> ExportResource:
        return ExportResource(self._client)

    @cached_property
    def valves(self) -> ValvesResource:
        return ValvesResource(self._client)

    @cached_property
    def with_raw_response(self) -> FunctionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return FunctionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FunctionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return FunctionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        id: str,
        content: str,
        meta: function_create_params.Meta,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionResponse]:
        """
        Create New Function

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/functions/create",
            body=maybe_transform(
                {
                    "id": id,
                    "content": content,
                    "meta": meta,
                    "name": name,
                },
                function_create_params.FunctionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionModel]:
        """
        Get Function By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/functions/id/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionModel,
        )

    def update(
        self,
        *,
        path_id: str,
        body_id: str,
        content: str,
        meta: function_update_params.Meta,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionModel]:
        """
        Update Function By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_id:
            raise ValueError(f"Expected a non-empty value for `path_id` but received {path_id!r}")
        return self._post(
            f"/functions/id/{path_id}/update",
            body=maybe_transform(
                {
                    "id": body_id,
                    "content": content,
                    "meta": meta,
                    "name": name,
                },
                function_update_params.FunctionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionModel,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionListResponse:
        """Get Functions"""
        return self._get(
            "/functions/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionDeleteResponse:
        """
        Delete Function By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            f"/functions/id/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionDeleteResponse,
        )

    def toggle(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionModel]:
        """
        Toggle Function By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/functions/id/{id}/toggle",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionModel,
        )

    def toggle_global(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionModel]:
        """
        Toggle Global By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/functions/id/{id}/toggle/global",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionModel,
        )


class AsyncFunctionsResource(AsyncAPIResource):
    @cached_property
    def export(self) -> AsyncExportResource:
        return AsyncExportResource(self._client)

    @cached_property
    def valves(self) -> AsyncValvesResource:
        return AsyncValvesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFunctionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFunctionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFunctionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncFunctionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        id: str,
        content: str,
        meta: function_create_params.Meta,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionResponse]:
        """
        Create New Function

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/functions/create",
            body=await async_maybe_transform(
                {
                    "id": id,
                    "content": content,
                    "meta": meta,
                    "name": name,
                },
                function_create_params.FunctionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionModel]:
        """
        Get Function By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/functions/id/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionModel,
        )

    async def update(
        self,
        *,
        path_id: str,
        body_id: str,
        content: str,
        meta: function_update_params.Meta,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionModel]:
        """
        Update Function By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_id:
            raise ValueError(f"Expected a non-empty value for `path_id` but received {path_id!r}")
        return await self._post(
            f"/functions/id/{path_id}/update",
            body=await async_maybe_transform(
                {
                    "id": body_id,
                    "content": content,
                    "meta": meta,
                    "name": name,
                },
                function_update_params.FunctionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionModel,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionListResponse:
        """Get Functions"""
        return await self._get(
            "/functions/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FunctionDeleteResponse:
        """
        Delete Function By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            f"/functions/id/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionDeleteResponse,
        )

    async def toggle(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionModel]:
        """
        Toggle Function By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/functions/id/{id}/toggle",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionModel,
        )

    async def toggle_global(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[FunctionModel]:
        """
        Toggle Global By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/functions/id/{id}/toggle/global",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FunctionModel,
        )


class FunctionsResourceWithRawResponse:
    def __init__(self, functions: FunctionsResource) -> None:
        self._functions = functions

        self.create = to_raw_response_wrapper(
            functions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            functions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            functions.update,
        )
        self.list = to_raw_response_wrapper(
            functions.list,
        )
        self.delete = to_raw_response_wrapper(
            functions.delete,
        )
        self.toggle = to_raw_response_wrapper(
            functions.toggle,
        )
        self.toggle_global = to_raw_response_wrapper(
            functions.toggle_global,
        )

    @cached_property
    def export(self) -> ExportResourceWithRawResponse:
        return ExportResourceWithRawResponse(self._functions.export)

    @cached_property
    def valves(self) -> ValvesResourceWithRawResponse:
        return ValvesResourceWithRawResponse(self._functions.valves)


class AsyncFunctionsResourceWithRawResponse:
    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self._functions = functions

        self.create = async_to_raw_response_wrapper(
            functions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            functions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            functions.update,
        )
        self.list = async_to_raw_response_wrapper(
            functions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            functions.delete,
        )
        self.toggle = async_to_raw_response_wrapper(
            functions.toggle,
        )
        self.toggle_global = async_to_raw_response_wrapper(
            functions.toggle_global,
        )

    @cached_property
    def export(self) -> AsyncExportResourceWithRawResponse:
        return AsyncExportResourceWithRawResponse(self._functions.export)

    @cached_property
    def valves(self) -> AsyncValvesResourceWithRawResponse:
        return AsyncValvesResourceWithRawResponse(self._functions.valves)


class FunctionsResourceWithStreamingResponse:
    def __init__(self, functions: FunctionsResource) -> None:
        self._functions = functions

        self.create = to_streamed_response_wrapper(
            functions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            functions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            functions.update,
        )
        self.list = to_streamed_response_wrapper(
            functions.list,
        )
        self.delete = to_streamed_response_wrapper(
            functions.delete,
        )
        self.toggle = to_streamed_response_wrapper(
            functions.toggle,
        )
        self.toggle_global = to_streamed_response_wrapper(
            functions.toggle_global,
        )

    @cached_property
    def export(self) -> ExportResourceWithStreamingResponse:
        return ExportResourceWithStreamingResponse(self._functions.export)

    @cached_property
    def valves(self) -> ValvesResourceWithStreamingResponse:
        return ValvesResourceWithStreamingResponse(self._functions.valves)


class AsyncFunctionsResourceWithStreamingResponse:
    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self._functions = functions

        self.create = async_to_streamed_response_wrapper(
            functions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            functions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            functions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            functions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            functions.delete,
        )
        self.toggle = async_to_streamed_response_wrapper(
            functions.toggle,
        )
        self.toggle_global = async_to_streamed_response_wrapper(
            functions.toggle_global,
        )

    @cached_property
    def export(self) -> AsyncExportResourceWithStreamingResponse:
        return AsyncExportResourceWithStreamingResponse(self._functions.export)

    @cached_property
    def valves(self) -> AsyncValvesResourceWithStreamingResponse:
        return AsyncValvesResourceWithStreamingResponse(self._functions.valves)
