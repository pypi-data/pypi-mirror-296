# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ToolModel", "Meta"]


class Meta(BaseModel):
    description: Optional[str] = None

    manifest: Optional[object] = None


class ToolModel(BaseModel):
    id: str

    content: str

    created_at: int

    meta: Meta

    name: str

    specs: List[object]

    updated_at: int

    user_id: str
