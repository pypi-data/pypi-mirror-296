# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMarkdown:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Pyopenwebui) -> None:
        markdown = client.utils.markdown.create(
            md="md",
        )
        assert_matches_type(object, markdown, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Pyopenwebui) -> None:
        response = client.utils.markdown.with_raw_response.create(
            md="md",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        markdown = response.parse()
        assert_matches_type(object, markdown, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Pyopenwebui) -> None:
        with client.utils.markdown.with_streaming_response.create(
            md="md",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            markdown = response.parse()
            assert_matches_type(object, markdown, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMarkdown:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncPyopenwebui) -> None:
        markdown = await async_client.utils.markdown.create(
            md="md",
        )
        assert_matches_type(object, markdown, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.utils.markdown.with_raw_response.create(
            md="md",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        markdown = await response.parse()
        assert_matches_type(object, markdown, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.utils.markdown.with_streaming_response.create(
            md="md",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            markdown = await response.parse()
            assert_matches_type(object, markdown, path=["response"])

        assert cast(Any, response.is_closed) is True
