# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AuthUpdateProfileParams"]


class AuthUpdateProfileParams(TypedDict, total=False):
    name: Required[str]

    profile_image_url: Required[str]
