# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["AuthSignupParams"]


class AuthSignupParams(TypedDict, total=False):
    email: Required[str]

    name: Required[str]

    password: Required[str]

    profile_image_url: Optional[str]
