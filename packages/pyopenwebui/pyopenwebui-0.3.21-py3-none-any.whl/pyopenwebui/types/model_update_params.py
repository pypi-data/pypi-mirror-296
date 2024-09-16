# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = ["ModelUpdateParams", "Meta"]


class ModelUpdateParams(TypedDict, total=False):
    query_id: Required[Annotated[str, PropertyInfo(alias="id")]]

    body_id: Required[Annotated[str, PropertyInfo(alias="id")]]

    meta: Required[Meta]

    name: Required[str]

    params: Required[Dict[str, object]]

    base_model_id: Optional[str]


class MetaTyped(TypedDict, total=False):
    capabilities: Optional[object]

    description: Optional[str]

    profile_image_url: Optional[str]


Meta: TypeAlias = Union[MetaTyped, Dict[str, object]]
