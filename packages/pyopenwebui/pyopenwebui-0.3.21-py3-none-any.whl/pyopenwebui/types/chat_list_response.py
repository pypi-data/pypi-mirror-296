# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .chat_title_id_response import ChatTitleIDResponse

__all__ = ["ChatListResponse"]

ChatListResponse: TypeAlias = List[ChatTitleIDResponse]
