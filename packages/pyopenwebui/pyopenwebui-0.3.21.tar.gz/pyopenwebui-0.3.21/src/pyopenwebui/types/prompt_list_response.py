# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .shared.prompt_model import PromptModel

__all__ = ["PromptListResponse"]

PromptListResponse: TypeAlias = List[PromptModel]
