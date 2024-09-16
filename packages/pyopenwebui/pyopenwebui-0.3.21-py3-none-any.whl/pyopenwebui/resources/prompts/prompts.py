# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...types import prompt_create_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .commands import (
    CommandsResource,
    AsyncCommandsResource,
    CommandsResourceWithRawResponse,
    AsyncCommandsResourceWithRawResponse,
    CommandsResourceWithStreamingResponse,
    AsyncCommandsResourceWithStreamingResponse,
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
from ...types.shared.prompt_model import PromptModel
from ...types.prompt_list_response import PromptListResponse

__all__ = ["PromptsResource", "AsyncPromptsResource"]


class PromptsResource(SyncAPIResource):
    @cached_property
    def commands(self) -> CommandsResource:
        return CommandsResource(self._client)

    @cached_property
    def with_raw_response(self) -> PromptsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return PromptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PromptsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return PromptsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        command: str,
        content: str,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[PromptModel]:
        """
        Create New Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/prompts/create",
            body=maybe_transform(
                {
                    "command": command,
                    "content": content,
                    "title": title,
                },
                prompt_create_params.PromptCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptModel,
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
    ) -> PromptListResponse:
        """Get Prompts"""
        return self._get(
            "/prompts/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptListResponse,
        )


class AsyncPromptsResource(AsyncAPIResource):
    @cached_property
    def commands(self) -> AsyncCommandsResource:
        return AsyncCommandsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPromptsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPromptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPromptsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncPromptsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        command: str,
        content: str,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[PromptModel]:
        """
        Create New Prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/prompts/create",
            body=await async_maybe_transform(
                {
                    "command": command,
                    "content": content,
                    "title": title,
                },
                prompt_create_params.PromptCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptModel,
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
    ) -> PromptListResponse:
        """Get Prompts"""
        return await self._get(
            "/prompts/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptListResponse,
        )


class PromptsResourceWithRawResponse:
    def __init__(self, prompts: PromptsResource) -> None:
        self._prompts = prompts

        self.create = to_raw_response_wrapper(
            prompts.create,
        )
        self.list = to_raw_response_wrapper(
            prompts.list,
        )

    @cached_property
    def commands(self) -> CommandsResourceWithRawResponse:
        return CommandsResourceWithRawResponse(self._prompts.commands)


class AsyncPromptsResourceWithRawResponse:
    def __init__(self, prompts: AsyncPromptsResource) -> None:
        self._prompts = prompts

        self.create = async_to_raw_response_wrapper(
            prompts.create,
        )
        self.list = async_to_raw_response_wrapper(
            prompts.list,
        )

    @cached_property
    def commands(self) -> AsyncCommandsResourceWithRawResponse:
        return AsyncCommandsResourceWithRawResponse(self._prompts.commands)


class PromptsResourceWithStreamingResponse:
    def __init__(self, prompts: PromptsResource) -> None:
        self._prompts = prompts

        self.create = to_streamed_response_wrapper(
            prompts.create,
        )
        self.list = to_streamed_response_wrapper(
            prompts.list,
        )

    @cached_property
    def commands(self) -> CommandsResourceWithStreamingResponse:
        return CommandsResourceWithStreamingResponse(self._prompts.commands)


class AsyncPromptsResourceWithStreamingResponse:
    def __init__(self, prompts: AsyncPromptsResource) -> None:
        self._prompts = prompts

        self.create = async_to_streamed_response_wrapper(
            prompts.create,
        )
        self.list = async_to_streamed_response_wrapper(
            prompts.list,
        )

    @cached_property
    def commands(self) -> AsyncCommandsResourceWithStreamingResponse:
        return AsyncCommandsResourceWithStreamingResponse(self._prompts.commands)
