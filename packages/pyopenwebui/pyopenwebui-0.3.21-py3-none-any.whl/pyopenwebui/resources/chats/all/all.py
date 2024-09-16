# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .db import (
    DBResource,
    AsyncDBResource,
    DBResourceWithRawResponse,
    AsyncDBResourceWithRawResponse,
    DBResourceWithStreamingResponse,
    AsyncDBResourceWithStreamingResponse,
)
from .archived import (
    ArchivedResource,
    AsyncArchivedResource,
    ArchivedResourceWithRawResponse,
    AsyncArchivedResourceWithRawResponse,
    ArchivedResourceWithStreamingResponse,
    AsyncArchivedResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["AllResource", "AsyncAllResource"]


class AllResource(SyncAPIResource):
    @cached_property
    def archived(self) -> ArchivedResource:
        return ArchivedResource(self._client)

    @cached_property
    def db(self) -> DBResource:
        return DBResource(self._client)

    @cached_property
    def with_raw_response(self) -> AllResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AllResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AllResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AllResourceWithStreamingResponse(self)


class AsyncAllResource(AsyncAPIResource):
    @cached_property
    def archived(self) -> AsyncArchivedResource:
        return AsyncArchivedResource(self._client)

    @cached_property
    def db(self) -> AsyncDBResource:
        return AsyncDBResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAllResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAllResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAllResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncAllResourceWithStreamingResponse(self)


class AllResourceWithRawResponse:
    def __init__(self, all: AllResource) -> None:
        self._all = all

    @cached_property
    def archived(self) -> ArchivedResourceWithRawResponse:
        return ArchivedResourceWithRawResponse(self._all.archived)

    @cached_property
    def db(self) -> DBResourceWithRawResponse:
        return DBResourceWithRawResponse(self._all.db)


class AsyncAllResourceWithRawResponse:
    def __init__(self, all: AsyncAllResource) -> None:
        self._all = all

    @cached_property
    def archived(self) -> AsyncArchivedResourceWithRawResponse:
        return AsyncArchivedResourceWithRawResponse(self._all.archived)

    @cached_property
    def db(self) -> AsyncDBResourceWithRawResponse:
        return AsyncDBResourceWithRawResponse(self._all.db)


class AllResourceWithStreamingResponse:
    def __init__(self, all: AllResource) -> None:
        self._all = all

    @cached_property
    def archived(self) -> ArchivedResourceWithStreamingResponse:
        return ArchivedResourceWithStreamingResponse(self._all.archived)

    @cached_property
    def db(self) -> DBResourceWithStreamingResponse:
        return DBResourceWithStreamingResponse(self._all.db)


class AsyncAllResourceWithStreamingResponse:
    def __init__(self, all: AsyncAllResource) -> None:
        self._all = all

    @cached_property
    def archived(self) -> AsyncArchivedResourceWithStreamingResponse:
        return AsyncArchivedResourceWithStreamingResponse(self._all.archived)

    @cached_property
    def db(self) -> AsyncDBResourceWithStreamingResponse:
        return AsyncDBResourceWithStreamingResponse(self._all.db)
