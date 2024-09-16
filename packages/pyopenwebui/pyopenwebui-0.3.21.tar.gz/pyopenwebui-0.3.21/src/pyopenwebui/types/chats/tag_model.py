# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["TagModel"]


class TagModel(BaseModel):
    id: str

    name: str

    user_id: str

    data: Optional[str] = None
