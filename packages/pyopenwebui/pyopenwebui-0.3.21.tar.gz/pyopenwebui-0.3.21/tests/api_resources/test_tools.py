# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types import (
    ToolModel,
    ToolResponse,
    ToolListResponse,
    ToolDeleteResponse,
    ToolExportResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTools:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Pyopenwebui) -> None:
        tool = client.tools.create(
            id="id",
            content="content",
            meta={},
            name="name",
        )
        assert_matches_type(Optional[ToolResponse], tool, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Pyopenwebui) -> None:
        tool = client.tools.create(
            id="id",
            content="content",
            meta={
                "description": "description",
                "manifest": {},
            },
            name="name",
        )
        assert_matches_type(Optional[ToolResponse], tool, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Pyopenwebui) -> None:
        response = client.tools.with_raw_response.create(
            id="id",
            content="content",
            meta={},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(Optional[ToolResponse], tool, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Pyopenwebui) -> None:
        with client.tools.with_streaming_response.create(
            id="id",
            content="content",
            meta={},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(Optional[ToolResponse], tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Pyopenwebui) -> None:
        tool = client.tools.retrieve(
            "id",
        )
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Pyopenwebui) -> None:
        response = client.tools.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Pyopenwebui) -> None:
        with client.tools.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(Optional[ToolModel], tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.tools.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Pyopenwebui) -> None:
        tool = client.tools.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        )
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Pyopenwebui) -> None:
        tool = client.tools.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={
                "description": "description",
                "manifest": {},
            },
            name="name",
        )
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Pyopenwebui) -> None:
        response = client.tools.with_raw_response.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Pyopenwebui) -> None:
        with client.tools.with_streaming_response.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(Optional[ToolModel], tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            client.tools.with_raw_response.update(
                path_id="",
                body_id="",
                content="content",
                meta={},
                name="name",
            )

    @parametrize
    def test_method_list(self, client: Pyopenwebui) -> None:
        tool = client.tools.list()
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Pyopenwebui) -> None:
        response = client.tools.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Pyopenwebui) -> None:
        with client.tools.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(ToolListResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Pyopenwebui) -> None:
        tool = client.tools.delete(
            "id",
        )
        assert_matches_type(ToolDeleteResponse, tool, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Pyopenwebui) -> None:
        response = client.tools.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(ToolDeleteResponse, tool, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Pyopenwebui) -> None:
        with client.tools.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(ToolDeleteResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.tools.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_export(self, client: Pyopenwebui) -> None:
        tool = client.tools.export()
        assert_matches_type(ToolExportResponse, tool, path=["response"])

    @parametrize
    def test_raw_response_export(self, client: Pyopenwebui) -> None:
        response = client.tools.with_raw_response.export()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(ToolExportResponse, tool, path=["response"])

    @parametrize
    def test_streaming_response_export(self, client: Pyopenwebui) -> None:
        with client.tools.with_streaming_response.export() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(ToolExportResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTools:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncPyopenwebui) -> None:
        tool = await async_client.tools.create(
            id="id",
            content="content",
            meta={},
            name="name",
        )
        assert_matches_type(Optional[ToolResponse], tool, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        tool = await async_client.tools.create(
            id="id",
            content="content",
            meta={
                "description": "description",
                "manifest": {},
            },
            name="name",
        )
        assert_matches_type(Optional[ToolResponse], tool, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.tools.with_raw_response.create(
            id="id",
            content="content",
            meta={},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(Optional[ToolResponse], tool, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.tools.with_streaming_response.create(
            id="id",
            content="content",
            meta={},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(Optional[ToolResponse], tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        tool = await async_client.tools.retrieve(
            "id",
        )
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.tools.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.tools.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(Optional[ToolModel], tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.tools.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncPyopenwebui) -> None:
        tool = await async_client.tools.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        )
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        tool = await async_client.tools.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={
                "description": "description",
                "manifest": {},
            },
            name="name",
        )
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.tools.with_raw_response.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(Optional[ToolModel], tool, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.tools.with_streaming_response.update(
            path_id="id",
            body_id="id",
            content="content",
            meta={},
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(Optional[ToolModel], tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            await async_client.tools.with_raw_response.update(
                path_id="",
                body_id="",
                content="content",
                meta={},
                name="name",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPyopenwebui) -> None:
        tool = await async_client.tools.list()
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.tools.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.tools.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(ToolListResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPyopenwebui) -> None:
        tool = await async_client.tools.delete(
            "id",
        )
        assert_matches_type(ToolDeleteResponse, tool, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.tools.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(ToolDeleteResponse, tool, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.tools.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(ToolDeleteResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.tools.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_export(self, async_client: AsyncPyopenwebui) -> None:
        tool = await async_client.tools.export()
        assert_matches_type(ToolExportResponse, tool, path=["response"])

    @parametrize
    async def test_raw_response_export(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.tools.with_raw_response.export()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(ToolExportResponse, tool, path=["response"])

    @parametrize
    async def test_streaming_response_export(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.tools.with_streaming_response.export() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(ToolExportResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True
