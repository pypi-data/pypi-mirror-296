# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from .._models import BaseModel

__all__ = ["ChatTitleIDResponse"]


class ChatTitleIDResponse(BaseModel):
    id: str

    created_at: int

    title: str

    updated_at: int
