# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .prompt_suggestion_param import PromptSuggestionParam

__all__ = ["SuggestionCreateParams"]


class SuggestionCreateParams(TypedDict, total=False):
    suggestions: Required[Iterable[PromptSuggestionParam]]
