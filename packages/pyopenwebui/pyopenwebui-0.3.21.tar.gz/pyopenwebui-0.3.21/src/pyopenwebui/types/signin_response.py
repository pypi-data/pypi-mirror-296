# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from .._models import BaseModel

__all__ = ["SigninResponse"]


class SigninResponse(BaseModel):
    id: str

    token: str

    email: str

    name: str

    profile_image_url: str

    role: str

    token_type: str
