# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types.shared import DocumentResponse
from pyopenwebui.types.documents import DocDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDoc:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Pyopenwebui) -> None:
        doc = client.documents.doc.retrieve(
            name="name",
        )
        assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Pyopenwebui) -> None:
        response = client.documents.doc.with_raw_response.retrieve(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        doc = response.parse()
        assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Pyopenwebui) -> None:
        with client.documents.doc.with_streaming_response.retrieve(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            doc = response.parse()
            assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Pyopenwebui) -> None:
        doc = client.documents.doc.update(
            query_name="name",
            body_name="name",
            title="title",
        )
        assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Pyopenwebui) -> None:
        response = client.documents.doc.with_raw_response.update(
            query_name="name",
            body_name="name",
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        doc = response.parse()
        assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Pyopenwebui) -> None:
        with client.documents.doc.with_streaming_response.update(
            query_name="name",
            body_name="name",
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            doc = response.parse()
            assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Pyopenwebui) -> None:
        doc = client.documents.doc.delete(
            name="name",
        )
        assert_matches_type(DocDeleteResponse, doc, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Pyopenwebui) -> None:
        response = client.documents.doc.with_raw_response.delete(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        doc = response.parse()
        assert_matches_type(DocDeleteResponse, doc, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Pyopenwebui) -> None:
        with client.documents.doc.with_streaming_response.delete(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            doc = response.parse()
            assert_matches_type(DocDeleteResponse, doc, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDoc:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        doc = await async_client.documents.doc.retrieve(
            name="name",
        )
        assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.documents.doc.with_raw_response.retrieve(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        doc = await response.parse()
        assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.documents.doc.with_streaming_response.retrieve(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            doc = await response.parse()
            assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncPyopenwebui) -> None:
        doc = await async_client.documents.doc.update(
            query_name="name",
            body_name="name",
            title="title",
        )
        assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.documents.doc.with_raw_response.update(
            query_name="name",
            body_name="name",
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        doc = await response.parse()
        assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.documents.doc.with_streaming_response.update(
            query_name="name",
            body_name="name",
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            doc = await response.parse()
            assert_matches_type(Optional[DocumentResponse], doc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPyopenwebui) -> None:
        doc = await async_client.documents.doc.delete(
            name="name",
        )
        assert_matches_type(DocDeleteResponse, doc, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.documents.doc.with_raw_response.delete(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        doc = await response.parse()
        assert_matches_type(DocDeleteResponse, doc, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.documents.doc.with_streaming_response.delete(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            doc = await response.parse()
            assert_matches_type(DocDeleteResponse, doc, path=["response"])

        assert cast(Any, response.is_closed) is True
