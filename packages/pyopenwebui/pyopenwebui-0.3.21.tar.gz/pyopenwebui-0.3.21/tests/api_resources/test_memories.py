# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types import (
    MemoryModel,
    MemoryListResponse,
    MemoryResetResponse,
    MemoryDeleteResponse,
    MemoryDeleteUserResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMemories:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: Pyopenwebui) -> None:
        memory = client.memories.update(
            memory_id="memory_id",
        )
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Pyopenwebui) -> None:
        memory = client.memories.update(
            memory_id="memory_id",
            content="content",
        )
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Pyopenwebui) -> None:
        response = client.memories.with_raw_response.update(
            memory_id="memory_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Pyopenwebui) -> None:
        with client.memories.with_streaming_response.update(
            memory_id="memory_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(Optional[MemoryModel], memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            client.memories.with_raw_response.update(
                memory_id="",
            )

    @parametrize
    def test_method_list(self, client: Pyopenwebui) -> None:
        memory = client.memories.list()
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Pyopenwebui) -> None:
        response = client.memories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Pyopenwebui) -> None:
        with client.memories.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryListResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Pyopenwebui) -> None:
        memory = client.memories.delete(
            "memory_id",
        )
        assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Pyopenwebui) -> None:
        response = client.memories.with_raw_response.delete(
            "memory_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Pyopenwebui) -> None:
        with client.memories.with_streaming_response.delete(
            "memory_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            client.memories.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_add(self, client: Pyopenwebui) -> None:
        memory = client.memories.add(
            content="content",
        )
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: Pyopenwebui) -> None:
        response = client.memories.with_raw_response.add(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: Pyopenwebui) -> None:
        with client.memories.with_streaming_response.add(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(Optional[MemoryModel], memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete_user(self, client: Pyopenwebui) -> None:
        memory = client.memories.delete_user()
        assert_matches_type(MemoryDeleteUserResponse, memory, path=["response"])

    @parametrize
    def test_raw_response_delete_user(self, client: Pyopenwebui) -> None:
        response = client.memories.with_raw_response.delete_user()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryDeleteUserResponse, memory, path=["response"])

    @parametrize
    def test_streaming_response_delete_user(self, client: Pyopenwebui) -> None:
        with client.memories.with_streaming_response.delete_user() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryDeleteUserResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_query(self, client: Pyopenwebui) -> None:
        memory = client.memories.query(
            content="content",
        )
        assert_matches_type(object, memory, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: Pyopenwebui) -> None:
        memory = client.memories.query(
            content="content",
            k=0,
        )
        assert_matches_type(object, memory, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: Pyopenwebui) -> None:
        response = client.memories.with_raw_response.query(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(object, memory, path=["response"])

    @parametrize
    def test_streaming_response_query(self, client: Pyopenwebui) -> None:
        with client.memories.with_streaming_response.query(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(object, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_reset(self, client: Pyopenwebui) -> None:
        memory = client.memories.reset()
        assert_matches_type(MemoryResetResponse, memory, path=["response"])

    @parametrize
    def test_raw_response_reset(self, client: Pyopenwebui) -> None:
        response = client.memories.with_raw_response.reset()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryResetResponse, memory, path=["response"])

    @parametrize
    def test_streaming_response_reset(self, client: Pyopenwebui) -> None:
        with client.memories.with_streaming_response.reset() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryResetResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMemories:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.update(
            memory_id="memory_id",
        )
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.update(
            memory_id="memory_id",
            content="content",
        )
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.memories.with_raw_response.update(
            memory_id="memory_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.memories.with_streaming_response.update(
            memory_id="memory_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(Optional[MemoryModel], memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            await async_client.memories.with_raw_response.update(
                memory_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.list()
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.memories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.memories.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryListResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.delete(
            "memory_id",
        )
        assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.memories.with_raw_response.delete(
            "memory_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.memories.with_streaming_response.delete(
            "memory_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `memory_id` but received ''"):
            await async_client.memories.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_add(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.add(
            content="content",
        )
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.memories.with_raw_response.add(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(Optional[MemoryModel], memory, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.memories.with_streaming_response.add(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(Optional[MemoryModel], memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete_user(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.delete_user()
        assert_matches_type(MemoryDeleteUserResponse, memory, path=["response"])

    @parametrize
    async def test_raw_response_delete_user(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.memories.with_raw_response.delete_user()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryDeleteUserResponse, memory, path=["response"])

    @parametrize
    async def test_streaming_response_delete_user(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.memories.with_streaming_response.delete_user() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryDeleteUserResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_query(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.query(
            content="content",
        )
        assert_matches_type(object, memory, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.query(
            content="content",
            k=0,
        )
        assert_matches_type(object, memory, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.memories.with_raw_response.query(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(object, memory, path=["response"])

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.memories.with_streaming_response.query(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(object, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_reset(self, async_client: AsyncPyopenwebui) -> None:
        memory = await async_client.memories.reset()
        assert_matches_type(MemoryResetResponse, memory, path=["response"])

    @parametrize
    async def test_raw_response_reset(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.memories.with_raw_response.reset()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryResetResponse, memory, path=["response"])

    @parametrize
    async def test_streaming_response_reset(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.memories.with_streaming_response.reset() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryResetResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True
