# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

from ..train_eval_dataset_param import TrainEvalDatasetParam
from ..shared_params.sampling_params import SamplingParams

__all__ = ["QuestionAnsweringCreateParams", "Request"]


class QuestionAnsweringCreateParams(TypedDict, total=False):
    request: Required[Request]


class Request(TypedDict, total=False):
    checkpoint: Required[object]
    """Checkpoint created during training runs"""

    dataset: Required[TrainEvalDatasetParam]

    job_uuid: Required[str]

    metrics: Required[List[Literal["em", "f1"]]]

    sampling_params: Required[SamplingParams]
