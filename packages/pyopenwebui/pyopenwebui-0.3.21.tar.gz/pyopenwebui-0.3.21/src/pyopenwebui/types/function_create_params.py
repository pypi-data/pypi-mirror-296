# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["FunctionCreateParams", "Meta"]


class FunctionCreateParams(TypedDict, total=False):
    id: Required[str]

    content: Required[str]

    meta: Required[Meta]

    name: Required[str]


class Meta(TypedDict, total=False):
    description: Optional[str]

    manifest: Optional[object]
