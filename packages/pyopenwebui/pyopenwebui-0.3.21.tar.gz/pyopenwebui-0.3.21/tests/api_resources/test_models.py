# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types import (
    ModelModel,
    ModelDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: Pyopenwebui) -> None:
        model = client.models.update(
            query_id="id",
            body_id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Pyopenwebui) -> None:
        model = client.models.update(
            query_id="id",
            body_id="id",
            meta={
                "capabilities": {},
                "description": "description",
                "profile_image_url": "profile_image_url",
            },
            name="name",
            params={"foo": "bar"},
            base_model_id="base_model_id",
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Pyopenwebui) -> None:
        response = client.models.with_raw_response.update(
            query_id="id",
            body_id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Pyopenwebui) -> None:
        with client.models.with_streaming_response.update(
            query_id="id",
            body_id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(Optional[ModelModel], model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Pyopenwebui) -> None:
        model = client.models.list(
            id="id",
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Pyopenwebui) -> None:
        response = client.models.with_raw_response.list(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Pyopenwebui) -> None:
        with client.models.with_streaming_response.list(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(Optional[ModelModel], model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Pyopenwebui) -> None:
        model = client.models.delete(
            id="id",
        )
        assert_matches_type(ModelDeleteResponse, model, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Pyopenwebui) -> None:
        response = client.models.with_raw_response.delete(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelDeleteResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Pyopenwebui) -> None:
        with client.models.with_streaming_response.delete(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelDeleteResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_add(self, client: Pyopenwebui) -> None:
        model = client.models.add(
            id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    def test_method_add_with_all_params(self, client: Pyopenwebui) -> None:
        model = client.models.add(
            id="id",
            meta={
                "capabilities": {},
                "description": "description",
                "profile_image_url": "profile_image_url",
            },
            name="name",
            params={"foo": "bar"},
            base_model_id="base_model_id",
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: Pyopenwebui) -> None:
        response = client.models.with_raw_response.add(
            id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: Pyopenwebui) -> None:
        with client.models.with_streaming_response.add(
            id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(Optional[ModelModel], model, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncModels:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update(self, async_client: AsyncPyopenwebui) -> None:
        model = await async_client.models.update(
            query_id="id",
            body_id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        model = await async_client.models.update(
            query_id="id",
            body_id="id",
            meta={
                "capabilities": {},
                "description": "description",
                "profile_image_url": "profile_image_url",
            },
            name="name",
            params={"foo": "bar"},
            base_model_id="base_model_id",
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.models.with_raw_response.update(
            query_id="id",
            body_id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.models.with_streaming_response.update(
            query_id="id",
            body_id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(Optional[ModelModel], model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncPyopenwebui) -> None:
        model = await async_client.models.list(
            id="id",
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.models.with_raw_response.list(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.models.with_streaming_response.list(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(Optional[ModelModel], model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPyopenwebui) -> None:
        model = await async_client.models.delete(
            id="id",
        )
        assert_matches_type(ModelDeleteResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.models.with_raw_response.delete(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelDeleteResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.models.with_streaming_response.delete(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelDeleteResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_add(self, async_client: AsyncPyopenwebui) -> None:
        model = await async_client.models.add(
            id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncPyopenwebui) -> None:
        model = await async_client.models.add(
            id="id",
            meta={
                "capabilities": {},
                "description": "description",
                "profile_image_url": "profile_image_url",
            },
            name="name",
            params={"foo": "bar"},
            base_model_id="base_model_id",
        )
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.models.with_raw_response.add(
            id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(Optional[ModelModel], model, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.models.with_streaming_response.add(
            id="id",
            meta={},
            name="name",
            params={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(Optional[ModelModel], model, path=["response"])

        assert cast(Any, response.is_closed) is True
