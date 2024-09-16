# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from .._models import BaseModel

__all__ = ["MemoryModel"]


class MemoryModel(BaseModel):
    id: str

    content: str

    created_at: int

    updated_at: int

    user_id: str
