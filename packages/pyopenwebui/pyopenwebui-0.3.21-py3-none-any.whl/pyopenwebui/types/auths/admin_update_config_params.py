# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["AdminUpdateConfigParams"]


class AdminUpdateConfigParams(TypedDict, total=False):
    default_user_role: Required[Annotated[str, PropertyInfo(alias="DEFAULT_USER_ROLE")]]

    enable_community_sharing: Required[Annotated[bool, PropertyInfo(alias="ENABLE_COMMUNITY_SHARING")]]

    enable_message_rating: Required[Annotated[bool, PropertyInfo(alias="ENABLE_MESSAGE_RATING")]]

    enable_signup: Required[Annotated[bool, PropertyInfo(alias="ENABLE_SIGNUP")]]

    jwt_expires_in: Required[Annotated[str, PropertyInfo(alias="JWT_EXPIRES_IN")]]

    show_admin_details: Required[Annotated[bool, PropertyInfo(alias="SHOW_ADMIN_DETAILS")]]
