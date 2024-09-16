# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DocumentCreateParams"]


class DocumentCreateParams(TypedDict, total=False):
    collection_name: Required[str]

    filename: Required[str]

    name: Required[str]

    title: Required[str]

    content: Optional[str]
