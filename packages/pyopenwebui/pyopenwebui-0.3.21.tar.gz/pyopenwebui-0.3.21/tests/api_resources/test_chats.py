# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types import (
    ChatResponse,
    ChatListResponse,
    ChatDeleteResponse,
    ChatListAllResponse,
    ChatUnshareResponse,
    ChatListUserResponse,
    ChatArchiveAllResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChats:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Pyopenwebui) -> None:
        chat = client.chats.create(
            id="id",
            chat={},
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.create(
            id="id",
            chat={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.create(
            id="id",
            chat={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.with_raw_response.create(
                id="",
                chat={},
            )

    @parametrize
    def test_method_retrieve(self, client: Pyopenwebui) -> None:
        chat = client.chats.retrieve(
            "id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Pyopenwebui) -> None:
        chat = client.chats.list()
        assert_matches_type(ChatListResponse, chat, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Pyopenwebui) -> None:
        chat = client.chats.list(
            page=0,
        )
        assert_matches_type(ChatListResponse, chat, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatListResponse, chat, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatListResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Pyopenwebui) -> None:
        chat = client.chats.delete(
            "id",
        )
        assert_matches_type(ChatDeleteResponse, chat, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatDeleteResponse, chat, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatDeleteResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_archive(self, client: Pyopenwebui) -> None:
        chat = client.chats.archive(
            "id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.archive(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.archive(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.with_raw_response.archive(
                "",
            )

    @parametrize
    def test_method_archive_all(self, client: Pyopenwebui) -> None:
        chat = client.chats.archive_all()
        assert_matches_type(ChatArchiveAllResponse, chat, path=["response"])

    @parametrize
    def test_raw_response_archive_all(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.archive_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatArchiveAllResponse, chat, path=["response"])

    @parametrize
    def test_streaming_response_archive_all(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.archive_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatArchiveAllResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_clone(self, client: Pyopenwebui) -> None:
        chat = client.chats.clone(
            "id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_raw_response_clone(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.clone(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_streaming_response_clone(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.clone(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_clone(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.with_raw_response.clone(
                "",
            )

    @parametrize
    def test_method_list_all(self, client: Pyopenwebui) -> None:
        chat = client.chats.list_all()
        assert_matches_type(ChatListAllResponse, chat, path=["response"])

    @parametrize
    def test_raw_response_list_all(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.list_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatListAllResponse, chat, path=["response"])

    @parametrize
    def test_streaming_response_list_all(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.list_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatListAllResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_user(self, client: Pyopenwebui) -> None:
        chat = client.chats.list_user(
            user_id="user_id",
        )
        assert_matches_type(ChatListUserResponse, chat, path=["response"])

    @parametrize
    def test_method_list_user_with_all_params(self, client: Pyopenwebui) -> None:
        chat = client.chats.list_user(
            user_id="user_id",
            limit=0,
            skip=0,
        )
        assert_matches_type(ChatListUserResponse, chat, path=["response"])

    @parametrize
    def test_raw_response_list_user(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.list_user(
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatListUserResponse, chat, path=["response"])

    @parametrize
    def test_streaming_response_list_user(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.list_user(
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatListUserResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list_user(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.chats.with_raw_response.list_user(
                user_id="",
            )

    @parametrize
    def test_method_retrieve_share(self, client: Pyopenwebui) -> None:
        chat = client.chats.retrieve_share(
            "share_id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_raw_response_retrieve_share(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.retrieve_share(
            "share_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_share(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.retrieve_share(
            "share_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve_share(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `share_id` but received ''"):
            client.chats.with_raw_response.retrieve_share(
                "",
            )

    @parametrize
    def test_method_share(self, client: Pyopenwebui) -> None:
        chat = client.chats.share(
            "id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_raw_response_share(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.share(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    def test_streaming_response_share(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.share(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_share(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.with_raw_response.share(
                "",
            )

    @parametrize
    def test_method_unshare(self, client: Pyopenwebui) -> None:
        chat = client.chats.unshare(
            "id",
        )
        assert_matches_type(Optional[ChatUnshareResponse], chat, path=["response"])

    @parametrize
    def test_raw_response_unshare(self, client: Pyopenwebui) -> None:
        response = client.chats.with_raw_response.unshare(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(Optional[ChatUnshareResponse], chat, path=["response"])

    @parametrize
    def test_streaming_response_unshare(self, client: Pyopenwebui) -> None:
        with client.chats.with_streaming_response.unshare(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(Optional[ChatUnshareResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_unshare(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chats.with_raw_response.unshare(
                "",
            )


class TestAsyncChats:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.create(
            id="id",
            chat={},
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.create(
            id="id",
            chat={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.create(
            id="id",
            chat={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.with_raw_response.create(
                id="",
                chat={},
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.retrieve(
            "id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.list()
        assert_matches_type(ChatListResponse, chat, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.list(
            page=0,
        )
        assert_matches_type(ChatListResponse, chat, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatListResponse, chat, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatListResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.delete(
            "id",
        )
        assert_matches_type(ChatDeleteResponse, chat, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatDeleteResponse, chat, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatDeleteResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.archive(
            "id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.archive(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.archive(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.with_raw_response.archive(
                "",
            )

    @parametrize
    async def test_method_archive_all(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.archive_all()
        assert_matches_type(ChatArchiveAllResponse, chat, path=["response"])

    @parametrize
    async def test_raw_response_archive_all(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.archive_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatArchiveAllResponse, chat, path=["response"])

    @parametrize
    async def test_streaming_response_archive_all(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.archive_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatArchiveAllResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_clone(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.clone(
            "id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_raw_response_clone(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.clone(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_streaming_response_clone(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.clone(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_clone(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.with_raw_response.clone(
                "",
            )

    @parametrize
    async def test_method_list_all(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.list_all()
        assert_matches_type(ChatListAllResponse, chat, path=["response"])

    @parametrize
    async def test_raw_response_list_all(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.list_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatListAllResponse, chat, path=["response"])

    @parametrize
    async def test_streaming_response_list_all(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.list_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatListAllResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_user(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.list_user(
            user_id="user_id",
        )
        assert_matches_type(ChatListUserResponse, chat, path=["response"])

    @parametrize
    async def test_method_list_user_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.list_user(
            user_id="user_id",
            limit=0,
            skip=0,
        )
        assert_matches_type(ChatListUserResponse, chat, path=["response"])

    @parametrize
    async def test_raw_response_list_user(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.list_user(
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatListUserResponse, chat, path=["response"])

    @parametrize
    async def test_streaming_response_list_user(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.list_user(
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatListUserResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list_user(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.chats.with_raw_response.list_user(
                user_id="",
            )

    @parametrize
    async def test_method_retrieve_share(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.retrieve_share(
            "share_id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_share(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.retrieve_share(
            "share_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_share(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.retrieve_share(
            "share_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve_share(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `share_id` but received ''"):
            await async_client.chats.with_raw_response.retrieve_share(
                "",
            )

    @parametrize
    async def test_method_share(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.share(
            "id",
        )
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_raw_response_share(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.share(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(Optional[ChatResponse], chat, path=["response"])

    @parametrize
    async def test_streaming_response_share(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.share(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(Optional[ChatResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_share(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.with_raw_response.share(
                "",
            )

    @parametrize
    async def test_method_unshare(self, async_client: AsyncPyopenwebui) -> None:
        chat = await async_client.chats.unshare(
            "id",
        )
        assert_matches_type(Optional[ChatUnshareResponse], chat, path=["response"])

    @parametrize
    async def test_raw_response_unshare(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.with_raw_response.unshare(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(Optional[ChatUnshareResponse], chat, path=["response"])

    @parametrize
    async def test_streaming_response_unshare(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.with_streaming_response.unshare(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(Optional[ChatUnshareResponse], chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_unshare(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chats.with_raw_response.unshare(
                "",
            )
