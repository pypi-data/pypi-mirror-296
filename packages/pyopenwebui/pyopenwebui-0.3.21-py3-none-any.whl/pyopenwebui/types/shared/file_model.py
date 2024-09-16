# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from ..._models import BaseModel

__all__ = ["FileModel"]


class FileModel(BaseModel):
    id: str

    created_at: int

    filename: str

    meta: object

    user_id: str
