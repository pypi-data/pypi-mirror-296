# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ChatResponse"]


class ChatResponse(BaseModel):
    id: str

    archived: bool

    chat: object

    created_at: int

    title: str

    updated_at: int

    user_id: str

    share_id: Optional[str] = None
