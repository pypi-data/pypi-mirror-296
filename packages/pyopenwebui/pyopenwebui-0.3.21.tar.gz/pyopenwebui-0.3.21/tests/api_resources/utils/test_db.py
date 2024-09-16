# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDB:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_download(self, client: Pyopenwebui) -> None:
        db = client.utils.db.download()
        assert_matches_type(object, db, path=["response"])

    @parametrize
    def test_raw_response_download(self, client: Pyopenwebui) -> None:
        response = client.utils.db.with_raw_response.download()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        db = response.parse()
        assert_matches_type(object, db, path=["response"])

    @parametrize
    def test_streaming_response_download(self, client: Pyopenwebui) -> None:
        with client.utils.db.with_streaming_response.download() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            db = response.parse()
            assert_matches_type(object, db, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDB:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_download(self, async_client: AsyncPyopenwebui) -> None:
        db = await async_client.utils.db.download()
        assert_matches_type(object, db, path=["response"])

    @parametrize
    async def test_raw_response_download(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.utils.db.with_raw_response.download()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        db = await response.parse()
        assert_matches_type(object, db, path=["response"])

    @parametrize
    async def test_streaming_response_download(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.utils.db.with_streaming_response.download() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            db = await response.parse()
            assert_matches_type(object, db, path=["response"])

        assert cast(Any, response.is_closed) is True
