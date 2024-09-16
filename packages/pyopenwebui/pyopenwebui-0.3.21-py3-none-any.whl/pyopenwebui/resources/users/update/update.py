# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .role import (
    RoleResource,
    AsyncRoleResource,
    RoleResourceWithRawResponse,
    AsyncRoleResourceWithRawResponse,
    RoleResourceWithStreamingResponse,
    AsyncRoleResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["UpdateResource", "AsyncUpdateResource"]


class UpdateResource(SyncAPIResource):
    @cached_property
    def role(self) -> RoleResource:
        return RoleResource(self._client)

    @cached_property
    def with_raw_response(self) -> UpdateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return UpdateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UpdateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return UpdateResourceWithStreamingResponse(self)


class AsyncUpdateResource(AsyncAPIResource):
    @cached_property
    def role(self) -> AsyncRoleResource:
        return AsyncRoleResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncUpdateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUpdateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUpdateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncUpdateResourceWithStreamingResponse(self)


class UpdateResourceWithRawResponse:
    def __init__(self, update: UpdateResource) -> None:
        self._update = update

    @cached_property
    def role(self) -> RoleResourceWithRawResponse:
        return RoleResourceWithRawResponse(self._update.role)


class AsyncUpdateResourceWithRawResponse:
    def __init__(self, update: AsyncUpdateResource) -> None:
        self._update = update

    @cached_property
    def role(self) -> AsyncRoleResourceWithRawResponse:
        return AsyncRoleResourceWithRawResponse(self._update.role)


class UpdateResourceWithStreamingResponse:
    def __init__(self, update: UpdateResource) -> None:
        self._update = update

    @cached_property
    def role(self) -> RoleResourceWithStreamingResponse:
        return RoleResourceWithStreamingResponse(self._update.role)


class AsyncUpdateResourceWithStreamingResponse:
    def __init__(self, update: AsyncUpdateResource) -> None:
        self._update = update

    @cached_property
    def role(self) -> AsyncRoleResourceWithStreamingResponse:
        return AsyncRoleResourceWithStreamingResponse(self._update.role)
