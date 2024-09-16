# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types import (
    FunctionModel,
    FunctionResponse,
    FunctionListResponse,
    FunctionDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFunctions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Pyopenwebui) -> None:
        function = client.functions.create(
            id="id",
            content="content",
            meta={},
            name="name",
        )
        assert_matches_type(Optional[FunctionResponse], function, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Pyopenwebui) -> None:
        function = client.functions.create(
            id="id",
            content="content",
            meta={
                "description": "description",
                "manifest": {},
            },
            name="name",
        )
        assert_matches_type(Optional[FunctionResponse], function, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Pyopenwebui) -> None:
        response = client.functions.with_raw_response.create(
            id="id",
            content="content",
            meta={},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(Optional[FunctionResponse], function, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Pyopenwebui) -> None:
        with client.functions.with_streaming_response.create(
            id="id",
            content="content",
            meta={},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(Optional[FunctionResponse], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Pyopenwebui) -> None:
        function = client.functions.retrieve(
            "id",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Pyopenwebui) -> None:
        response = client.functions.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Pyopenwebui) -> None:
        with client.functions.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(Optional[FunctionModel], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.functions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Pyopenwebui) -> None:
        function = client.functions.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Pyopenwebui) -> None:
        function = client.functions.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={
                "description": "description",
                "manifest": {},
            },
            name="name",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Pyopenwebui) -> None:
        response = client.functions.with_raw_response.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Pyopenwebui) -> None:
        with client.functions.with_streaming_response.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(Optional[FunctionModel], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            client.functions.with_raw_response.update(
                path_id="",
                body_id="",
                content="content",
                meta={},
                name="name",
            )

    @parametrize
    def test_method_list(self, client: Pyopenwebui) -> None:
        function = client.functions.list()
        assert_matches_type(FunctionListResponse, function, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Pyopenwebui) -> None:
        response = client.functions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(FunctionListResponse, function, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Pyopenwebui) -> None:
        with client.functions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(FunctionListResponse, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Pyopenwebui) -> None:
        function = client.functions.delete(
            "id",
        )
        assert_matches_type(FunctionDeleteResponse, function, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Pyopenwebui) -> None:
        response = client.functions.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(FunctionDeleteResponse, function, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Pyopenwebui) -> None:
        with client.functions.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(FunctionDeleteResponse, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.functions.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_toggle(self, client: Pyopenwebui) -> None:
        function = client.functions.toggle(
            "id",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_raw_response_toggle(self, client: Pyopenwebui) -> None:
        response = client.functions.with_raw_response.toggle(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_streaming_response_toggle(self, client: Pyopenwebui) -> None:
        with client.functions.with_streaming_response.toggle(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(Optional[FunctionModel], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_toggle(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.functions.with_raw_response.toggle(
                "",
            )

    @parametrize
    def test_method_toggle_global(self, client: Pyopenwebui) -> None:
        function = client.functions.toggle_global(
            "id",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_raw_response_toggle_global(self, client: Pyopenwebui) -> None:
        response = client.functions.with_raw_response.toggle_global(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    def test_streaming_response_toggle_global(self, client: Pyopenwebui) -> None:
        with client.functions.with_streaming_response.toggle_global(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(Optional[FunctionModel], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_toggle_global(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.functions.with_raw_response.toggle_global(
                "",
            )


class TestAsyncFunctions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.create(
            id="id",
            content="content",
            meta={},
            name="name",
        )
        assert_matches_type(Optional[FunctionResponse], function, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.create(
            id="id",
            content="content",
            meta={
                "description": "description",
                "manifest": {},
            },
            name="name",
        )
        assert_matches_type(Optional[FunctionResponse], function, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.functions.with_raw_response.create(
            id="id",
            content="content",
            meta={},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(Optional[FunctionResponse], function, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.functions.with_streaming_response.create(
            id="id",
            content="content",
            meta={},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(Optional[FunctionResponse], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.retrieve(
            "id",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.functions.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.functions.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(Optional[FunctionModel], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.functions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={
                "description": "description",
                "manifest": {},
            },
            name="name",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.functions.with_raw_response.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.functions.with_streaming_response.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(Optional[FunctionModel], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            await async_client.functions.with_raw_response.update(
                path_id="",
                body_id="",
                content="content",
                meta={},
                name="name",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.list()
        assert_matches_type(FunctionListResponse, function, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.functions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(FunctionListResponse, function, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.functions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(FunctionListResponse, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.delete(
            "id",
        )
        assert_matches_type(FunctionDeleteResponse, function, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.functions.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(FunctionDeleteResponse, function, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.functions.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(FunctionDeleteResponse, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.functions.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_toggle(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.toggle(
            "id",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_raw_response_toggle(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.functions.with_raw_response.toggle(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_streaming_response_toggle(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.functions.with_streaming_response.toggle(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(Optional[FunctionModel], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_toggle(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.functions.with_raw_response.toggle(
                "",
            )

    @parametrize
    async def test_method_toggle_global(self, async_client: AsyncPyopenwebui) -> None:
        function = await async_client.functions.toggle_global(
            "id",
        )
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_raw_response_toggle_global(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.functions.with_raw_response.toggle_global(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(Optional[FunctionModel], function, path=["response"])

    @parametrize
    async def test_streaming_response_toggle_global(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.functions.with_streaming_response.toggle_global(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(Optional[FunctionModel], function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_toggle_global(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.functions.with_raw_response.toggle_global(
                "",
            )
