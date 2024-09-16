# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types.chats import ArchivedListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestArchived:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Pyopenwebui) -> None:
        archived = client.chats.archived.list()
        assert_matches_type(ArchivedListResponse, archived, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Pyopenwebui) -> None:
        archived = client.chats.archived.list(
            limit=0,
            skip=0,
        )
        assert_matches_type(ArchivedListResponse, archived, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Pyopenwebui) -> None:
        response = client.chats.archived.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        archived = response.parse()
        assert_matches_type(ArchivedListResponse, archived, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Pyopenwebui) -> None:
        with client.chats.archived.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            archived = response.parse()
            assert_matches_type(ArchivedListResponse, archived, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncArchived:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncPyopenwebui) -> None:
        archived = await async_client.chats.archived.list()
        assert_matches_type(ArchivedListResponse, archived, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        archived = await async_client.chats.archived.list(
            limit=0,
            skip=0,
        )
        assert_matches_type(ArchivedListResponse, archived, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.chats.archived.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        archived = await response.parse()
        assert_matches_type(ArchivedListResponse, archived, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.chats.archived.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            archived = await response.parse()
            assert_matches_type(ArchivedListResponse, archived, path=["response"])

        assert cast(Any, response.is_closed) is True
