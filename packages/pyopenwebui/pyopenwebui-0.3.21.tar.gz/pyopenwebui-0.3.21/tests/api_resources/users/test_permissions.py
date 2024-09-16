# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPermissions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve_user(self, client: Pyopenwebui) -> None:
        permission = client.users.permissions.retrieve_user()
        assert_matches_type(object, permission, path=["response"])

    @parametrize
    def test_raw_response_retrieve_user(self, client: Pyopenwebui) -> None:
        response = client.users.permissions.with_raw_response.retrieve_user()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        permission = response.parse()
        assert_matches_type(object, permission, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_user(self, client: Pyopenwebui) -> None:
        with client.users.permissions.with_streaming_response.retrieve_user() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            permission = response.parse()
            assert_matches_type(object, permission, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPermissions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve_user(self, async_client: AsyncPyopenwebui) -> None:
        permission = await async_client.users.permissions.retrieve_user()
        assert_matches_type(object, permission, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_user(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.users.permissions.with_raw_response.retrieve_user()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        permission = await response.parse()
        assert_matches_type(object, permission, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_user(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.users.permissions.with_streaming_response.retrieve_user() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            permission = await response.parse()
            assert_matches_type(object, permission, path=["response"])

        assert cast(Any, response.is_closed) is True
