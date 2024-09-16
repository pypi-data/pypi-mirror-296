# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["BannerModel"]


class BannerModel(BaseModel):
    id: str

    content: str

    dismissible: bool

    timestamp: int

    type: str

    title: Optional[str] = None
