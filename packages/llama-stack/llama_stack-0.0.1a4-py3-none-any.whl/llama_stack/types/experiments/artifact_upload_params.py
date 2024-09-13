# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["ArtifactUploadParams", "Request"]


class ArtifactUploadParams(TypedDict, total=False):
    request: Required[Request]


class Request(TypedDict, total=False):
    artifact_type: Required[str]

    content: Required[str]

    experiment_id: Required[str]

    name: Required[str]

    metadata: Dict[str, Union[bool, float, str, Iterable[object], object, None]]
