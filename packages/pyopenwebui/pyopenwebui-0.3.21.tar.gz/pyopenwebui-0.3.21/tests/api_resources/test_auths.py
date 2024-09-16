# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types import (
    SigninResponse,
    AuthListResponse,
    AuthUpdateProfileResponse,
    AuthUpdatePasswordResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAuths:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Pyopenwebui) -> None:
        auth = client.auths.list()
        assert_matches_type(AuthListResponse, auth, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Pyopenwebui) -> None:
        response = client.auths.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthListResponse, auth, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Pyopenwebui) -> None:
        with client.auths.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthListResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_add(self, client: Pyopenwebui) -> None:
        auth = client.auths.add(
            email="email",
            name="name",
            password="password",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    def test_method_add_with_all_params(self, client: Pyopenwebui) -> None:
        auth = client.auths.add(
            email="email",
            name="name",
            password="password",
            profile_image_url="profile_image_url",
            role="role",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: Pyopenwebui) -> None:
        response = client.auths.with_raw_response.add(
            email="email",
            name="name",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: Pyopenwebui) -> None:
        with client.auths.with_streaming_response.add(
            email="email",
            name="name",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(SigninResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_signin(self, client: Pyopenwebui) -> None:
        auth = client.auths.signin(
            email="email",
            password="password",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    def test_raw_response_signin(self, client: Pyopenwebui) -> None:
        response = client.auths.with_raw_response.signin(
            email="email",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    def test_streaming_response_signin(self, client: Pyopenwebui) -> None:
        with client.auths.with_streaming_response.signin(
            email="email",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(SigninResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_signup(self, client: Pyopenwebui) -> None:
        auth = client.auths.signup(
            email="email",
            name="name",
            password="password",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    def test_method_signup_with_all_params(self, client: Pyopenwebui) -> None:
        auth = client.auths.signup(
            email="email",
            name="name",
            password="password",
            profile_image_url="profile_image_url",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    def test_raw_response_signup(self, client: Pyopenwebui) -> None:
        response = client.auths.with_raw_response.signup(
            email="email",
            name="name",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    def test_streaming_response_signup(self, client: Pyopenwebui) -> None:
        with client.auths.with_streaming_response.signup(
            email="email",
            name="name",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(SigninResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update_password(self, client: Pyopenwebui) -> None:
        auth = client.auths.update_password(
            new_password="new_password",
            password="password",
        )
        assert_matches_type(AuthUpdatePasswordResponse, auth, path=["response"])

    @parametrize
    def test_raw_response_update_password(self, client: Pyopenwebui) -> None:
        response = client.auths.with_raw_response.update_password(
            new_password="new_password",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthUpdatePasswordResponse, auth, path=["response"])

    @parametrize
    def test_streaming_response_update_password(self, client: Pyopenwebui) -> None:
        with client.auths.with_streaming_response.update_password(
            new_password="new_password",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthUpdatePasswordResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update_profile(self, client: Pyopenwebui) -> None:
        auth = client.auths.update_profile(
            name="name",
            profile_image_url="profile_image_url",
        )
        assert_matches_type(AuthUpdateProfileResponse, auth, path=["response"])

    @parametrize
    def test_raw_response_update_profile(self, client: Pyopenwebui) -> None:
        response = client.auths.with_raw_response.update_profile(
            name="name",
            profile_image_url="profile_image_url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthUpdateProfileResponse, auth, path=["response"])

    @parametrize
    def test_streaming_response_update_profile(self, client: Pyopenwebui) -> None:
        with client.auths.with_streaming_response.update_profile(
            name="name",
            profile_image_url="profile_image_url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthUpdateProfileResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAuths:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncPyopenwebui) -> None:
        auth = await async_client.auths.list()
        assert_matches_type(AuthListResponse, auth, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthListResponse, auth, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthListResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_add(self, async_client: AsyncPyopenwebui) -> None:
        auth = await async_client.auths.add(
            email="email",
            name="name",
            password="password",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        auth = await async_client.auths.add(
            email="email",
            name="name",
            password="password",
            profile_image_url="profile_image_url",
            role="role",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.with_raw_response.add(
            email="email",
            name="name",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.with_streaming_response.add(
            email="email",
            name="name",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(SigninResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_signin(self, async_client: AsyncPyopenwebui) -> None:
        auth = await async_client.auths.signin(
            email="email",
            password="password",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    async def test_raw_response_signin(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.with_raw_response.signin(
            email="email",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    async def test_streaming_response_signin(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.with_streaming_response.signin(
            email="email",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(SigninResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_signup(self, async_client: AsyncPyopenwebui) -> None:
        auth = await async_client.auths.signup(
            email="email",
            name="name",
            password="password",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    async def test_method_signup_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        auth = await async_client.auths.signup(
            email="email",
            name="name",
            password="password",
            profile_image_url="profile_image_url",
        )
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    async def test_raw_response_signup(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.with_raw_response.signup(
            email="email",
            name="name",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(SigninResponse, auth, path=["response"])

    @parametrize
    async def test_streaming_response_signup(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.with_streaming_response.signup(
            email="email",
            name="name",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(SigninResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update_password(self, async_client: AsyncPyopenwebui) -> None:
        auth = await async_client.auths.update_password(
            new_password="new_password",
            password="password",
        )
        assert_matches_type(AuthUpdatePasswordResponse, auth, path=["response"])

    @parametrize
    async def test_raw_response_update_password(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.with_raw_response.update_password(
            new_password="new_password",
            password="password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthUpdatePasswordResponse, auth, path=["response"])

    @parametrize
    async def test_streaming_response_update_password(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.with_streaming_response.update_password(
            new_password="new_password",
            password="password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthUpdatePasswordResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update_profile(self, async_client: AsyncPyopenwebui) -> None:
        auth = await async_client.auths.update_profile(
            name="name",
            profile_image_url="profile_image_url",
        )
        assert_matches_type(AuthUpdateProfileResponse, auth, path=["response"])

    @parametrize
    async def test_raw_response_update_profile(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.auths.with_raw_response.update_profile(
            name="name",
            profile_image_url="profile_image_url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthUpdateProfileResponse, auth, path=["response"])

    @parametrize
    async def test_streaming_response_update_profile(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.auths.with_streaming_response.update_profile(
            name="name",
            profile_image_url="profile_image_url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthUpdateProfileResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True
