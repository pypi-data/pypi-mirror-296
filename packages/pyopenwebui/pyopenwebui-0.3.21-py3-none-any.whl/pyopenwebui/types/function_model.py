# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["FunctionModel", "Meta"]


class Meta(BaseModel):
    description: Optional[str] = None

    manifest: Optional[object] = None


class FunctionModel(BaseModel):
    id: str

    content: str

    created_at: int

    meta: Meta

    name: str

    type: str

    updated_at: int

    user_id: str

    is_active: Optional[bool] = None

    is_global: Optional[bool] = None
