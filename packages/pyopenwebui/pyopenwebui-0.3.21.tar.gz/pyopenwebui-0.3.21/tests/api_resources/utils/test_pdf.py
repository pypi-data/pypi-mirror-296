# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPdf:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Pyopenwebui) -> None:
        pdf = client.utils.pdf.create(
            messages=[{}, {}, {}],
            title="title",
        )
        assert_matches_type(object, pdf, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Pyopenwebui) -> None:
        response = client.utils.pdf.with_raw_response.create(
            messages=[{}, {}, {}],
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pdf = response.parse()
        assert_matches_type(object, pdf, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Pyopenwebui) -> None:
        with client.utils.pdf.with_streaming_response.create(
            messages=[{}, {}, {}],
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pdf = response.parse()
            assert_matches_type(object, pdf, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPdf:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncPyopenwebui) -> None:
        pdf = await async_client.utils.pdf.create(
            messages=[{}, {}, {}],
            title="title",
        )
        assert_matches_type(object, pdf, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.utils.pdf.with_raw_response.create(
            messages=[{}, {}, {}],
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pdf = await response.parse()
        assert_matches_type(object, pdf, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.utils.pdf.with_streaming_response.create(
            messages=[{}, {}, {}],
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pdf = await response.parse()
            assert_matches_type(object, pdf, path=["response"])

        assert cast(Any, response.is_closed) is True
