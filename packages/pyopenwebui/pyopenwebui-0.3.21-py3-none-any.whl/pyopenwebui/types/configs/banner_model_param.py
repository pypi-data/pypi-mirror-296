# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["BannerModelParam"]


class BannerModelParam(TypedDict, total=False):
    id: Required[str]

    content: Required[str]

    dismissible: Required[bool]

    timestamp: Required[int]

    type: Required[str]

    title: Optional[str]
