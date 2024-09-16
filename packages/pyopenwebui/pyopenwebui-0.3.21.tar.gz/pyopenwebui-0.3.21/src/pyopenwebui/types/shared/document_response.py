# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["DocumentResponse"]


class DocumentResponse(BaseModel):
    collection_name: str

    filename: str

    name: str

    timestamp: int

    title: str

    user_id: str

    content: Optional[object] = None
