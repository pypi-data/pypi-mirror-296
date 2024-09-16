# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .users.user_settings import UserSettings

__all__ = ["UserModel"]


class UserModel(BaseModel):
    id: str

    created_at: int

    email: str

    last_active_at: int

    name: str

    profile_image_url: str

    updated_at: int

    api_key: Optional[str] = None

    info: Optional[object] = None

    oauth_sub: Optional[str] = None

    role: Optional[str] = None

    settings: Optional[UserSettings] = None
