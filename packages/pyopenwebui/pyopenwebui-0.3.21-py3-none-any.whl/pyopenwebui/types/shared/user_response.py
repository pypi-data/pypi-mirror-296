# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from ..._models import BaseModel

__all__ = ["UserResponse"]


class UserResponse(BaseModel):
    name: str

    profile_image_url: str
