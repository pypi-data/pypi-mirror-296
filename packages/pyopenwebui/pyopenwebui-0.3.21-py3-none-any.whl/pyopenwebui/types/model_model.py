# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, Optional

from .._models import BaseModel

__all__ = ["ModelModel", "Meta"]


class Meta(BaseModel):
    capabilities: Optional[object] = None

    description: Optional[str] = None

    profile_image_url: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ModelModel(BaseModel):
    id: str

    created_at: int

    meta: Meta

    name: str

    params: Dict[str, object]

    updated_at: int

    user_id: str

    base_model_id: Optional[str] = None
