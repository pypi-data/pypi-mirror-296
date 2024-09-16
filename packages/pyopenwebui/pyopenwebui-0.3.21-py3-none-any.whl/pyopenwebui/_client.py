# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "Pyopenwebui",
    "AsyncPyopenwebui",
    "Client",
    "AsyncClient",
]


class Pyopenwebui(SyncAPIClient):
    configs: resources.ConfigsResource
    auths: resources.AuthsResource
    users: resources.UsersResource
    chats: resources.ChatsResource
    documents: resources.DocumentsResource
    models: resources.ModelsResource
    prompts: resources.PromptsResource
    memories: resources.MemoriesResource
    files: resources.FilesResource
    tools: resources.ToolsResource
    functions: resources.FunctionsResource
    utils: resources.UtilsResource
    root: resources.RootResource
    with_raw_response: PyopenwebuiWithRawResponse
    with_streaming_response: PyopenwebuiWithStreamedResponse

    # client options

    def __init__(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous pyopenwebui client instance."""
        if base_url is None:
            base_url = os.environ.get("PYOPENWEBUI_BASE_URL")
        if base_url is None:
            base_url = f"/api/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.configs = resources.ConfigsResource(self)
        self.auths = resources.AuthsResource(self)
        self.users = resources.UsersResource(self)
        self.chats = resources.ChatsResource(self)
        self.documents = resources.DocumentsResource(self)
        self.models = resources.ModelsResource(self)
        self.prompts = resources.PromptsResource(self)
        self.memories = resources.MemoriesResource(self)
        self.files = resources.FilesResource(self)
        self.tools = resources.ToolsResource(self)
        self.functions = resources.FunctionsResource(self)
        self.utils = resources.UtilsResource(self)
        self.root = resources.RootResource(self)
        self.with_raw_response = PyopenwebuiWithRawResponse(self)
        self.with_streaming_response = PyopenwebuiWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncPyopenwebui(AsyncAPIClient):
    configs: resources.AsyncConfigsResource
    auths: resources.AsyncAuthsResource
    users: resources.AsyncUsersResource
    chats: resources.AsyncChatsResource
    documents: resources.AsyncDocumentsResource
    models: resources.AsyncModelsResource
    prompts: resources.AsyncPromptsResource
    memories: resources.AsyncMemoriesResource
    files: resources.AsyncFilesResource
    tools: resources.AsyncToolsResource
    functions: resources.AsyncFunctionsResource
    utils: resources.AsyncUtilsResource
    root: resources.AsyncRootResource
    with_raw_response: AsyncPyopenwebuiWithRawResponse
    with_streaming_response: AsyncPyopenwebuiWithStreamedResponse

    # client options

    def __init__(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async pyopenwebui client instance."""
        if base_url is None:
            base_url = os.environ.get("PYOPENWEBUI_BASE_URL")
        if base_url is None:
            base_url = f"/api/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.configs = resources.AsyncConfigsResource(self)
        self.auths = resources.AsyncAuthsResource(self)
        self.users = resources.AsyncUsersResource(self)
        self.chats = resources.AsyncChatsResource(self)
        self.documents = resources.AsyncDocumentsResource(self)
        self.models = resources.AsyncModelsResource(self)
        self.prompts = resources.AsyncPromptsResource(self)
        self.memories = resources.AsyncMemoriesResource(self)
        self.files = resources.AsyncFilesResource(self)
        self.tools = resources.AsyncToolsResource(self)
        self.functions = resources.AsyncFunctionsResource(self)
        self.utils = resources.AsyncUtilsResource(self)
        self.root = resources.AsyncRootResource(self)
        self.with_raw_response = AsyncPyopenwebuiWithRawResponse(self)
        self.with_streaming_response = AsyncPyopenwebuiWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class PyopenwebuiWithRawResponse:
    def __init__(self, client: Pyopenwebui) -> None:
        self.configs = resources.ConfigsResourceWithRawResponse(client.configs)
        self.auths = resources.AuthsResourceWithRawResponse(client.auths)
        self.users = resources.UsersResourceWithRawResponse(client.users)
        self.chats = resources.ChatsResourceWithRawResponse(client.chats)
        self.documents = resources.DocumentsResourceWithRawResponse(client.documents)
        self.models = resources.ModelsResourceWithRawResponse(client.models)
        self.prompts = resources.PromptsResourceWithRawResponse(client.prompts)
        self.memories = resources.MemoriesResourceWithRawResponse(client.memories)
        self.files = resources.FilesResourceWithRawResponse(client.files)
        self.tools = resources.ToolsResourceWithRawResponse(client.tools)
        self.functions = resources.FunctionsResourceWithRawResponse(client.functions)
        self.utils = resources.UtilsResourceWithRawResponse(client.utils)
        self.root = resources.RootResourceWithRawResponse(client.root)


class AsyncPyopenwebuiWithRawResponse:
    def __init__(self, client: AsyncPyopenwebui) -> None:
        self.configs = resources.AsyncConfigsResourceWithRawResponse(client.configs)
        self.auths = resources.AsyncAuthsResourceWithRawResponse(client.auths)
        self.users = resources.AsyncUsersResourceWithRawResponse(client.users)
        self.chats = resources.AsyncChatsResourceWithRawResponse(client.chats)
        self.documents = resources.AsyncDocumentsResourceWithRawResponse(client.documents)
        self.models = resources.AsyncModelsResourceWithRawResponse(client.models)
        self.prompts = resources.AsyncPromptsResourceWithRawResponse(client.prompts)
        self.memories = resources.AsyncMemoriesResourceWithRawResponse(client.memories)
        self.files = resources.AsyncFilesResourceWithRawResponse(client.files)
        self.tools = resources.AsyncToolsResourceWithRawResponse(client.tools)
        self.functions = resources.AsyncFunctionsResourceWithRawResponse(client.functions)
        self.utils = resources.AsyncUtilsResourceWithRawResponse(client.utils)
        self.root = resources.AsyncRootResourceWithRawResponse(client.root)


class PyopenwebuiWithStreamedResponse:
    def __init__(self, client: Pyopenwebui) -> None:
        self.configs = resources.ConfigsResourceWithStreamingResponse(client.configs)
        self.auths = resources.AuthsResourceWithStreamingResponse(client.auths)
        self.users = resources.UsersResourceWithStreamingResponse(client.users)
        self.chats = resources.ChatsResourceWithStreamingResponse(client.chats)
        self.documents = resources.DocumentsResourceWithStreamingResponse(client.documents)
        self.models = resources.ModelsResourceWithStreamingResponse(client.models)
        self.prompts = resources.PromptsResourceWithStreamingResponse(client.prompts)
        self.memories = resources.MemoriesResourceWithStreamingResponse(client.memories)
        self.files = resources.FilesResourceWithStreamingResponse(client.files)
        self.tools = resources.ToolsResourceWithStreamingResponse(client.tools)
        self.functions = resources.FunctionsResourceWithStreamingResponse(client.functions)
        self.utils = resources.UtilsResourceWithStreamingResponse(client.utils)
        self.root = resources.RootResourceWithStreamingResponse(client.root)


class AsyncPyopenwebuiWithStreamedResponse:
    def __init__(self, client: AsyncPyopenwebui) -> None:
        self.configs = resources.AsyncConfigsResourceWithStreamingResponse(client.configs)
        self.auths = resources.AsyncAuthsResourceWithStreamingResponse(client.auths)
        self.users = resources.AsyncUsersResourceWithStreamingResponse(client.users)
        self.chats = resources.AsyncChatsResourceWithStreamingResponse(client.chats)
        self.documents = resources.AsyncDocumentsResourceWithStreamingResponse(client.documents)
        self.models = resources.AsyncModelsResourceWithStreamingResponse(client.models)
        self.prompts = resources.AsyncPromptsResourceWithStreamingResponse(client.prompts)
        self.memories = resources.AsyncMemoriesResourceWithStreamingResponse(client.memories)
        self.files = resources.AsyncFilesResourceWithStreamingResponse(client.files)
        self.tools = resources.AsyncToolsResourceWithStreamingResponse(client.tools)
        self.functions = resources.AsyncFunctionsResourceWithStreamingResponse(client.functions)
        self.utils = resources.AsyncUtilsResourceWithStreamingResponse(client.utils)
        self.root = resources.AsyncRootResourceWithStreamingResponse(client.root)


Client = Pyopenwebui

AsyncClient = AsyncPyopenwebui
