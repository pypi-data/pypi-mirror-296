# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from pyopenwebui import Pyopenwebui, AsyncPyopenwebui
from tests.utils import assert_matches_type
from pyopenwebui.types.shared import FileModel

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFileName:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Pyopenwebui) -> None:
        file_name = client.files.content.file_name.retrieve(
            file_name="file_name",
            id="id",
        )
        assert_matches_type(Optional[FileModel], file_name, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Pyopenwebui) -> None:
        response = client.files.content.file_name.with_raw_response.retrieve(
            file_name="file_name",
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file_name = response.parse()
        assert_matches_type(Optional[FileModel], file_name, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Pyopenwebui) -> None:
        with client.files.content.file_name.with_streaming_response.retrieve(
            file_name="file_name",
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file_name = response.parse()
            assert_matches_type(Optional[FileModel], file_name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Pyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.files.content.file_name.with_raw_response.retrieve(
                file_name="file_name",
                id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_name` but received ''"):
            client.files.content.file_name.with_raw_response.retrieve(
                file_name="",
                id="id",
            )


class TestAsyncFileName:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        file_name = await async_client.files.content.file_name.retrieve(
            file_name="file_name",
            id="id",
        )
        assert_matches_type(Optional[FileModel], file_name, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        response = await async_client.files.content.file_name.with_raw_response.retrieve(
            file_name="file_name",
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file_name = await response.parse()
        assert_matches_type(Optional[FileModel], file_name, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        async with async_client.files.content.file_name.with_streaming_response.retrieve(
            file_name="file_name",
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file_name = await response.parse()
            assert_matches_type(Optional[FileModel], file_name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPyopenwebui) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.files.content.file_name.with_raw_response.retrieve(
                file_name="file_name",
                id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_name` but received ''"):
            await async_client.files.content.file_name.with_raw_response.retrieve(
                file_name="",
                id="id",
            )
