# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Required, TypedDict

__all__ = ["Attachment"]


class Attachment(TypedDict, total=False):
    content: Required[Union[str, List[str]]]

    mime_type: Required[str]
