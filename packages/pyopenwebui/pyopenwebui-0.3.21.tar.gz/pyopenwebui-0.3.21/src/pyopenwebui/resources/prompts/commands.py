# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

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
from ..._base_client import make_request_options
from ...types.prompts import command_update_params
from ...types.shared.prompt_model import PromptModel
from ...types.prompts.command_delete_response import CommandDeleteResponse

__all__ = ["CommandsResource", "AsyncCommandsResource"]


class CommandsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CommandsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return CommandsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CommandsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return CommandsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        command: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[PromptModel]:
        """
        Get Prompt By Command

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not command:
            raise ValueError(f"Expected a non-empty value for `command` but received {command!r}")
        return self._get(
            f"/prompts/command/{command}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptModel,
        )

    def update(
        self,
        *,
        path_command: str,
        body_command: str,
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
        Update Prompt By Command

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_command:
            raise ValueError(f"Expected a non-empty value for `path_command` but received {path_command!r}")
        return self._post(
            f"/prompts/command/{path_command}/update",
            body=maybe_transform(
                {
                    "command": body_command,
                    "content": content,
                    "title": title,
                },
                command_update_params.CommandUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptModel,
        )

    def delete(
        self,
        command: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandDeleteResponse:
        """
        Delete Prompt By Command

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not command:
            raise ValueError(f"Expected a non-empty value for `command` but received {command!r}")
        return self._delete(
            f"/prompts/command/{command}/delete",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommandDeleteResponse,
        )


class AsyncCommandsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCommandsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCommandsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCommandsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncCommandsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        command: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Optional[PromptModel]:
        """
        Get Prompt By Command

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not command:
            raise ValueError(f"Expected a non-empty value for `command` but received {command!r}")
        return await self._get(
            f"/prompts/command/{command}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptModel,
        )

    async def update(
        self,
        *,
        path_command: str,
        body_command: str,
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
        Update Prompt By Command

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_command:
            raise ValueError(f"Expected a non-empty value for `path_command` but received {path_command!r}")
        return await self._post(
            f"/prompts/command/{path_command}/update",
            body=await async_maybe_transform(
                {
                    "command": body_command,
                    "content": content,
                    "title": title,
                },
                command_update_params.CommandUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptModel,
        )

    async def delete(
        self,
        command: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandDeleteResponse:
        """
        Delete Prompt By Command

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not command:
            raise ValueError(f"Expected a non-empty value for `command` but received {command!r}")
        return await self._delete(
            f"/prompts/command/{command}/delete",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommandDeleteResponse,
        )


class CommandsResourceWithRawResponse:
    def __init__(self, commands: CommandsResource) -> None:
        self._commands = commands

        self.retrieve = to_raw_response_wrapper(
            commands.retrieve,
        )
        self.update = to_raw_response_wrapper(
            commands.update,
        )
        self.delete = to_raw_response_wrapper(
            commands.delete,
        )


class AsyncCommandsResourceWithRawResponse:
    def __init__(self, commands: AsyncCommandsResource) -> None:
        self._commands = commands

        self.retrieve = async_to_raw_response_wrapper(
            commands.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            commands.update,
        )
        self.delete = async_to_raw_response_wrapper(
            commands.delete,
        )


class CommandsResourceWithStreamingResponse:
    def __init__(self, commands: CommandsResource) -> None:
        self._commands = commands

        self.retrieve = to_streamed_response_wrapper(
            commands.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            commands.update,
        )
        self.delete = to_streamed_response_wrapper(
            commands.delete,
        )


class AsyncCommandsResourceWithStreamingResponse:
    def __init__(self, commands: AsyncCommandsResource) -> None:
        self._commands = commands

        self.retrieve = async_to_streamed_response_wrapper(
            commands.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            commands.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            commands.delete,
        )
