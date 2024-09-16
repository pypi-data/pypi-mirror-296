# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ToolUpdateParams", "Meta"]


class ToolUpdateParams(TypedDict, total=False):
    path_id: Required[Annotated[str, PropertyInfo(alias="id")]]

    body_id: Required[Annotated[str, PropertyInfo(alias="id")]]

    content: Required[str]

    meta: Required[Meta]

    name: Required[str]


class Meta(TypedDict, total=False):
    description: Optional[str]

    manifest: Optional[object]
