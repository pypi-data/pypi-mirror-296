# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from ..._models import BaseModel

__all__ = ["PromptModel"]


class PromptModel(BaseModel):
    command: str

    content: str

    timestamp: int

    title: str

    user_id: str
