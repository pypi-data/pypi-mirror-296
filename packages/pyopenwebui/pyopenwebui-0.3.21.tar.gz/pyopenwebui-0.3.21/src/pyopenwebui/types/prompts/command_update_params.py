# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["CommandUpdateParams"]


class CommandUpdateParams(TypedDict, total=False):
    path_command: Required[Annotated[str, PropertyInfo(alias="command")]]

    body_command: Required[Annotated[str, PropertyInfo(alias="command")]]

    content: Required[str]

    title: Required[str]
