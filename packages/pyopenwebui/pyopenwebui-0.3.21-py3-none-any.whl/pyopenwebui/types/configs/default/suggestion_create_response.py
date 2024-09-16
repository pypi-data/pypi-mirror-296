# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .prompt_suggestion import PromptSuggestion

__all__ = ["SuggestionCreateResponse"]

SuggestionCreateResponse: TypeAlias = List[PromptSuggestion]
