# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types.configs.default import SuggestionCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSuggestions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Pyopenwebui) -> None:
        suggestion = client.configs.default.suggestions.create(
            suggestions=[
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
            ],
        )
        assert_matches_type(SuggestionCreateResponse, suggestion, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Pyopenwebui) -> None:
        response = client.configs.default.suggestions.with_raw_response.create(
            suggestions=[
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        suggestion = response.parse()
        assert_matches_type(SuggestionCreateResponse, suggestion, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Pyopenwebui) -> None:
        with client.configs.default.suggestions.with_streaming_response.create(
            suggestions=[
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            suggestion = response.parse()
            assert_matches_type(SuggestionCreateResponse, suggestion, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSuggestions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncPyopenwebui) -> None:
        suggestion = await async_client.configs.default.suggestions.create(
            suggestions=[
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
            ],
        )
        assert_matches_type(SuggestionCreateResponse, suggestion, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.configs.default.suggestions.with_raw_response.create(
            suggestions=[
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        suggestion = await response.parse()
        assert_matches_type(SuggestionCreateResponse, suggestion, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.configs.default.suggestions.with_streaming_response.create(
            suggestions=[
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
                {
                    "content": "content",
                    "title": ["string", "string", "string"],
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            suggestion = await response.parse()
            assert_matches_type(SuggestionCreateResponse, suggestion, path=["response"])

        assert cast(Any, response.is_closed) is True
