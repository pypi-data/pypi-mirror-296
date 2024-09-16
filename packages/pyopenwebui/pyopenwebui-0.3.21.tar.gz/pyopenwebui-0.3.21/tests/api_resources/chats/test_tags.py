# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types.chats import (
    ChatIDTagModel,
    TagListResponse,
    TagDeleteResponse,
    TagDeleteAllResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTags:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Pyopenwebui) -> None:
        tag = client.chats.tags.create(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        )
        assert_matches_type(Optional[ChatIDTagModel], tag, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Pyopenwebui) -> None:
        response = client.chats.tags.with_raw_response.create(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tag = response.parse()
        assert_matches_type(Optional[ChatIDTagModel], tag, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Pyopenwebui) -> None:
        with client.chats.tags.with_streaming_response.create(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tag = response.parse()
            assert_matches_type(Optional[ChatIDTagModel], tag, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.tags.with_raw_response.create(
                id="",
                chat_id="chat_id",
                tag_name="tag_name",
            )

    @parametrize
    def test_method_list(self, client: Pyopenwebui) -> None:
        tag = client.chats.tags.list(
            "id",
        )
        assert_matches_type(TagListResponse, tag, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Pyopenwebui) -> None:
        response = client.chats.tags.with_raw_response.list(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tag = response.parse()
        assert_matches_type(TagListResponse, tag, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Pyopenwebui) -> None:
        with client.chats.tags.with_streaming_response.list(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tag = response.parse()
            assert_matches_type(TagListResponse, tag, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.tags.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: Pyopenwebui) -> None:
        tag = client.chats.tags.delete(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        )
        assert_matches_type(Optional[TagDeleteResponse], tag, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Pyopenwebui) -> None:
        response = client.chats.tags.with_raw_response.delete(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tag = response.parse()
        assert_matches_type(Optional[TagDeleteResponse], tag, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Pyopenwebui) -> None:
        with client.chats.tags.with_streaming_response.delete(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tag = response.parse()
            assert_matches_type(Optional[TagDeleteResponse], tag, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.tags.with_raw_response.delete(
                id="",
                chat_id="chat_id",
                tag_name="tag_name",
            )

    @parametrize
    def test_method_delete_all(self, client: Pyopenwebui) -> None:
        tag = client.chats.tags.delete_all(
            "id",
        )
        assert_matches_type(Optional[TagDeleteAllResponse], tag, path=["response"])

    @parametrize
    def test_raw_response_delete_all(self, client: Pyopenwebui) -> None:
        response = client.chats.tags.with_raw_response.delete_all(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tag = response.parse()
        assert_matches_type(Optional[TagDeleteAllResponse], tag, path=["response"])

    @parametrize
    def test_streaming_response_delete_all(self, client: Pyopenwebui) -> None:
        with client.chats.tags.with_streaming_response.delete_all(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tag = response.parse()
            assert_matches_type(Optional[TagDeleteAllResponse], tag, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete_all(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.tags.with_raw_response.delete_all(
                "",
            )


class TestAsyncTags:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncPyopenwebui) -> None:
        tag = await async_client.chats.tags.create(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        )
        assert_matches_type(Optional[ChatIDTagModel], tag, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.tags.with_raw_response.create(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tag = await response.parse()
        assert_matches_type(Optional[ChatIDTagModel], tag, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.tags.with_streaming_response.create(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tag = await response.parse()
            assert_matches_type(Optional[ChatIDTagModel], tag, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.tags.with_raw_response.create(
                id="",
                chat_id="chat_id",
                tag_name="tag_name",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPyopenwebui) -> None:
        tag = await async_client.chats.tags.list(
            "id",
        )
        assert_matches_type(TagListResponse, tag, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.tags.with_raw_response.list(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tag = await response.parse()
        assert_matches_type(TagListResponse, tag, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.tags.with_streaming_response.list(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tag = await response.parse()
            assert_matches_type(TagListResponse, tag, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.tags.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncPyopenwebui) -> None:
        tag = await async_client.chats.tags.delete(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        )
        assert_matches_type(Optional[TagDeleteResponse], tag, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.tags.with_raw_response.delete(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tag = await response.parse()
        assert_matches_type(Optional[TagDeleteResponse], tag, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.tags.with_streaming_response.delete(
            id="id",
            chat_id="chat_id",
            tag_name="tag_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tag = await response.parse()
            assert_matches_type(Optional[TagDeleteResponse], tag, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.tags.with_raw_response.delete(
                id="",
                chat_id="chat_id",
                tag_name="tag_name",
            )

    @parametrize
    async def test_method_delete_all(self, async_client: AsyncPyopenwebui) -> None:
        tag = await async_client.chats.tags.delete_all(
            "id",
        )
        assert_matches_type(Optional[TagDeleteAllResponse], tag, path=["response"])

    @parametrize
    async def test_raw_response_delete_all(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.tags.with_raw_response.delete_all(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tag = await response.parse()
        assert_matches_type(Optional[TagDeleteAllResponse], tag, path=["response"])

    @parametrize
    async def test_streaming_response_delete_all(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.tags.with_streaming_response.delete_all(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tag = await response.parse()
            assert_matches_type(Optional[TagDeleteAllResponse], tag, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete_all(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.tags.with_raw_response.delete_all(
                "",
            )
