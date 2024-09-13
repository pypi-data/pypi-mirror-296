# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .train_eval_dataset_param import TrainEvalDatasetParam

__all__ = ["DatasetCreateParams", "Request"]


class DatasetCreateParams(TypedDict, total=False):
    request: Required[Request]


class Request(TypedDict, total=False):
    dataset: Required[TrainEvalDatasetParam]

    uuid: Required[str]
