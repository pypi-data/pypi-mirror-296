# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["FunctionResponse", "Meta"]


class Meta(BaseModel):
    description: Optional[str] = None

    manifest: Optional[object] = None


class FunctionResponse(BaseModel):
    id: str

    created_at: int

    is_active: bool

    is_global: bool

    meta: Meta

    name: str

    type: str

    updated_at: int

    user_id: str
