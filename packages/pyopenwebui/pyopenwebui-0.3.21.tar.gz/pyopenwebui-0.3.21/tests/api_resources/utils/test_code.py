# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCode:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_format(self, client: Pyopenwebui) -> None:
        code = client.utils.code.format(
            code="code",
        )
        assert_matches_type(object, code, path=["response"])

    @parametrize
    def test_raw_response_format(self, client: Pyopenwebui) -> None:
        response = client.utils.code.with_raw_response.format(
            code="code",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        code = response.parse()
        assert_matches_type(object, code, path=["response"])

    @parametrize
    def test_streaming_response_format(self, client: Pyopenwebui) -> None:
        with client.utils.code.with_streaming_response.format(
            code="code",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            code = response.parse()
            assert_matches_type(object, code, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCode:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_format(self, async_client: AsyncPyopenwebui) -> None:
        code = await async_client.utils.code.format(
            code="code",
        )
        assert_matches_type(object, code, path=["response"])

    @parametrize
    async def test_raw_response_format(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.utils.code.with_raw_response.format(
            code="code",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        code = await response.parse()
        assert_matches_type(object, code, path=["response"])

    @parametrize
    async def test_streaming_response_format(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.utils.code.with_streaming_response.format(
            code="code",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            code = await response.parse()
            assert_matches_type(object, code, path=["response"])

        assert cast(Any, response.is_closed) is True
