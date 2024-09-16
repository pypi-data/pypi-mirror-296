# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ...._models import BaseModel

__all__ = ["PromptSuggestion"]


class PromptSuggestion(BaseModel):
    content: str

    title: List[str]
