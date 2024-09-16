# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from ..._models import BaseModel

__all__ = ["ChatIDTagModel"]


class ChatIDTagModel(BaseModel):
    id: str

    chat_id: str

    tag_name: str

    timestamp: int

    user_id: str
