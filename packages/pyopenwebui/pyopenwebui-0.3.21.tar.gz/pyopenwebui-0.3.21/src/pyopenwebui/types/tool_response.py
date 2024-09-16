# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ToolResponse", "Meta"]


class Meta(BaseModel):
    description: Optional[str] = None

    manifest: Optional[object] = None


class ToolResponse(BaseModel):
    id: str

    created_at: int

    meta: Meta

    name: str

    updated_at: int

    user_id: str
