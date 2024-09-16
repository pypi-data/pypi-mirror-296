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
from .pdf import (
    PdfResource,
    AsyncPdfResource,
    PdfResourceWithRawResponse,
    AsyncPdfResourceWithRawResponse,
    PdfResourceWithStreamingResponse,
    AsyncPdfResourceWithStreamingResponse,
)
from .code import (
    CodeResource,
    AsyncCodeResource,
    CodeResourceWithRawResponse,
    AsyncCodeResourceWithRawResponse,
    CodeResourceWithStreamingResponse,
    AsyncCodeResourceWithStreamingResponse,
)
from .litellm import (
    LitellmResource,
    AsyncLitellmResource,
    LitellmResourceWithRawResponse,
    AsyncLitellmResourceWithRawResponse,
    LitellmResourceWithStreamingResponse,
    AsyncLitellmResourceWithStreamingResponse,
)
from .gravatar import (
    GravatarResource,
    AsyncGravatarResource,
    GravatarResourceWithRawResponse,
    AsyncGravatarResourceWithRawResponse,
    GravatarResourceWithStreamingResponse,
    AsyncGravatarResourceWithStreamingResponse,
)
from .markdown import (
    MarkdownResource,
    AsyncMarkdownResource,
    MarkdownResourceWithRawResponse,
    AsyncMarkdownResourceWithRawResponse,
    MarkdownResourceWithStreamingResponse,
    AsyncMarkdownResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .litellm.litellm import LitellmResource, AsyncLitellmResource

__all__ = ["UtilsResource", "AsyncUtilsResource"]


class UtilsResource(SyncAPIResource):
    @cached_property
    def gravatar(self) -> GravatarResource:
        return GravatarResource(self._client)

    @cached_property
    def code(self) -> CodeResource:
        return CodeResource(self._client)

    @cached_property
    def markdown(self) -> MarkdownResource:
        return MarkdownResource(self._client)

    @cached_property
    def pdf(self) -> PdfResource:
        return PdfResource(self._client)

    @cached_property
    def db(self) -> DBResource:
        return DBResource(self._client)

    @cached_property
    def litellm(self) -> LitellmResource:
        return LitellmResource(self._client)

    @cached_property
    def with_raw_response(self) -> UtilsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return UtilsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UtilsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return UtilsResourceWithStreamingResponse(self)


class AsyncUtilsResource(AsyncAPIResource):
    @cached_property
    def gravatar(self) -> AsyncGravatarResource:
        return AsyncGravatarResource(self._client)

    @cached_property
    def code(self) -> AsyncCodeResource:
        return AsyncCodeResource(self._client)

    @cached_property
    def markdown(self) -> AsyncMarkdownResource:
        return AsyncMarkdownResource(self._client)

    @cached_property
    def pdf(self) -> AsyncPdfResource:
        return AsyncPdfResource(self._client)

    @cached_property
    def db(self) -> AsyncDBResource:
        return AsyncDBResource(self._client)

    @cached_property
    def litellm(self) -> AsyncLitellmResource:
        return AsyncLitellmResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncUtilsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUtilsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUtilsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aigc-libs/pyopenwebui-python#with_streaming_response
        """
        return AsyncUtilsResourceWithStreamingResponse(self)


class UtilsResourceWithRawResponse:
    def __init__(self, utils: UtilsResource) -> None:
        self._utils = utils

    @cached_property
    def gravatar(self) -> GravatarResourceWithRawResponse:
        return GravatarResourceWithRawResponse(self._utils.gravatar)

    @cached_property
    def code(self) -> CodeResourceWithRawResponse:
        return CodeResourceWithRawResponse(self._utils.code)

    @cached_property
    def markdown(self) -> MarkdownResourceWithRawResponse:
        return MarkdownResourceWithRawResponse(self._utils.markdown)

    @cached_property
    def pdf(self) -> PdfResourceWithRawResponse:
        return PdfResourceWithRawResponse(self._utils.pdf)

    @cached_property
    def db(self) -> DBResourceWithRawResponse:
        return DBResourceWithRawResponse(self._utils.db)

    @cached_property
    def litellm(self) -> LitellmResourceWithRawResponse:
        return LitellmResourceWithRawResponse(self._utils.litellm)


class AsyncUtilsResourceWithRawResponse:
    def __init__(self, utils: AsyncUtilsResource) -> None:
        self._utils = utils

    @cached_property
    def gravatar(self) -> AsyncGravatarResourceWithRawResponse:
        return AsyncGravatarResourceWithRawResponse(self._utils.gravatar)

    @cached_property
    def code(self) -> AsyncCodeResourceWithRawResponse:
        return AsyncCodeResourceWithRawResponse(self._utils.code)

    @cached_property
    def markdown(self) -> AsyncMarkdownResourceWithRawResponse:
        return AsyncMarkdownResourceWithRawResponse(self._utils.markdown)

    @cached_property
    def pdf(self) -> AsyncPdfResourceWithRawResponse:
        return AsyncPdfResourceWithRawResponse(self._utils.pdf)

    @cached_property
    def db(self) -> AsyncDBResourceWithRawResponse:
        return AsyncDBResourceWithRawResponse(self._utils.db)

    @cached_property
    def litellm(self) -> AsyncLitellmResourceWithRawResponse:
        return AsyncLitellmResourceWithRawResponse(self._utils.litellm)


class UtilsResourceWithStreamingResponse:
    def __init__(self, utils: UtilsResource) -> None:
        self._utils = utils

    @cached_property
    def gravatar(self) -> GravatarResourceWithStreamingResponse:
        return GravatarResourceWithStreamingResponse(self._utils.gravatar)

    @cached_property
    def code(self) -> CodeResourceWithStreamingResponse:
        return CodeResourceWithStreamingResponse(self._utils.code)

    @cached_property
    def markdown(self) -> MarkdownResourceWithStreamingResponse:
        return MarkdownResourceWithStreamingResponse(self._utils.markdown)

    @cached_property
    def pdf(self) -> PdfResourceWithStreamingResponse:
        return PdfResourceWithStreamingResponse(self._utils.pdf)

    @cached_property
    def db(self) -> DBResourceWithStreamingResponse:
        return DBResourceWithStreamingResponse(self._utils.db)

    @cached_property
    def litellm(self) -> LitellmResourceWithStreamingResponse:
        return LitellmResourceWithStreamingResponse(self._utils.litellm)


class AsyncUtilsResourceWithStreamingResponse:
    def __init__(self, utils: AsyncUtilsResource) -> None:
        self._utils = utils

    @cached_property
    def gravatar(self) -> AsyncGravatarResourceWithStreamingResponse:
        return AsyncGravatarResourceWithStreamingResponse(self._utils.gravatar)

    @cached_property
    def code(self) -> AsyncCodeResourceWithStreamingResponse:
        return AsyncCodeResourceWithStreamingResponse(self._utils.code)

    @cached_property
    def markdown(self) -> AsyncMarkdownResourceWithStreamingResponse:
        return AsyncMarkdownResourceWithStreamingResponse(self._utils.markdown)

    @cached_property
    def pdf(self) -> AsyncPdfResourceWithStreamingResponse:
        return AsyncPdfResourceWithStreamingResponse(self._utils.pdf)

    @cached_property
    def db(self) -> AsyncDBResourceWithStreamingResponse:
        return AsyncDBResourceWithStreamingResponse(self._utils.db)

    @cached_property
    def litellm(self) -> AsyncLitellmResourceWithStreamingResponse:
        return AsyncLitellmResourceWithStreamingResponse(self._utils.litellm)
