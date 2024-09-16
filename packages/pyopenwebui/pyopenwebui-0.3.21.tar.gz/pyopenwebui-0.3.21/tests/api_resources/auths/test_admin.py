# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAdmin:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve_config(self, client: Pyopenwebui) -> None:
        admin = client.auths.admin.retrieve_config()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    def test_raw_response_retrieve_config(self, client: Pyopenwebui) -> None:
        response = client.auths.admin.with_raw_response.retrieve_config()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        admin = response.parse()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_config(self, client: Pyopenwebui) -> None:
        with client.auths.admin.with_streaming_response.retrieve_config() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            admin = response.parse()
            assert_matches_type(object, admin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve_details(self, client: Pyopenwebui) -> None:
        admin = client.auths.admin.retrieve_details()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    def test_raw_response_retrieve_details(self, client: Pyopenwebui) -> None:
        response = client.auths.admin.with_raw_response.retrieve_details()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        admin = response.parse()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_details(self, client: Pyopenwebui) -> None:
        with client.auths.admin.with_streaming_response.retrieve_details() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            admin = response.parse()
            assert_matches_type(object, admin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update_config(self, client: Pyopenwebui) -> None:
        admin = client.auths.admin.update_config(
            default_user_role="DEFAULT_USER_ROLE",
            enable_community_sharing=True,
            enable_message_rating=True,
            enable_signup=True,
            jwt_expires_in="JWT_EXPIRES_IN",
            show_admin_details=True,
        )
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    def test_raw_response_update_config(self, client: Pyopenwebui) -> None:
        response = client.auths.admin.with_raw_response.update_config(
            default_user_role="DEFAULT_USER_ROLE",
            enable_community_sharing=True,
            enable_message_rating=True,
            enable_signup=True,
            jwt_expires_in="JWT_EXPIRES_IN",
            show_admin_details=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        admin = response.parse()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    def test_streaming_response_update_config(self, client: Pyopenwebui) -> None:
        with client.auths.admin.with_streaming_response.update_config(
            default_user_role="DEFAULT_USER_ROLE",
            enable_community_sharing=True,
            enable_message_rating=True,
            enable_signup=True,
            jwt_expires_in="JWT_EXPIRES_IN",
            show_admin_details=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            admin = response.parse()
            assert_matches_type(object, admin, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAdmin:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve_config(self, async_client: AsyncPyopenwebui) -> None:
        admin = await async_client.auths.admin.retrieve_config()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_config(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.admin.with_raw_response.retrieve_config()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        admin = await response.parse()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_config(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.admin.with_streaming_response.retrieve_config() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            admin = await response.parse()
            assert_matches_type(object, admin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve_details(self, async_client: AsyncPyopenwebui) -> None:
        admin = await async_client.auths.admin.retrieve_details()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_details(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.admin.with_raw_response.retrieve_details()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        admin = await response.parse()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_details(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.admin.with_streaming_response.retrieve_details() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            admin = await response.parse()
            assert_matches_type(object, admin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update_config(self, async_client: AsyncPyopenwebui) -> None:
        admin = await async_client.auths.admin.update_config(
            default_user_role="DEFAULT_USER_ROLE",
            enable_community_sharing=True,
            enable_message_rating=True,
            enable_signup=True,
            jwt_expires_in="JWT_EXPIRES_IN",
            show_admin_details=True,
        )
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    async def test_raw_response_update_config(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.admin.with_raw_response.update_config(
            default_user_role="DEFAULT_USER_ROLE",
            enable_community_sharing=True,
            enable_message_rating=True,
            enable_signup=True,
            jwt_expires_in="JWT_EXPIRES_IN",
            show_admin_details=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        admin = await response.parse()
        assert_matches_type(object, admin, path=["response"])

    @parametrize
    async def test_streaming_response_update_config(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.admin.with_streaming_response.update_config(
            default_user_role="DEFAULT_USER_ROLE",
            enable_community_sharing=True,
            enable_message_rating=True,
            enable_signup=True,
            jwt_expires_in="JWT_EXPIRES_IN",
            show_admin_details=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            admin = await response.parse()
            assert_matches_type(object, admin, path=["response"])

        assert cast(Any, response.is_closed) is True
