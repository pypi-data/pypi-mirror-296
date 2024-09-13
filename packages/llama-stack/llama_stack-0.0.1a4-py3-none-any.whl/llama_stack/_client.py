# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Dict, Union, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "LlamaStack",
    "AsyncLlamaStack",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "http://any-hosted-llama-stack.com",
    "sandbox": "https://example.com",
}


class LlamaStack(SyncAPIClient):
    agentic_system: resources.AgenticSystemResource
    artifacts: resources.ArtifactsResource
    datasets: resources.DatasetsResource
    evaluate: resources.EvaluateResource
    evaluations: resources.EvaluationsResource
    experiments: resources.ExperimentsResource
    inference: resources.InferenceResource
    logging: resources.LoggingResource
    safety: resources.SafetyResource
    memory_banks: resources.MemoryBanksResource
    post_training: resources.PostTrainingResource
    reward_scoring: resources.RewardScoringResource
    runs: resources.RunsResource
    synthetic_data_generation: resources.SyntheticDataGenerationResource
    batch_inference: resources.BatchInferenceResource
    with_raw_response: LlamaStackWithRawResponse
    with_streaming_response: LlamaStackWithStreamedResponse

    # client options

    _environment: Literal["production", "sandbox"] | NotGiven

    def __init__(
        self,
        *,
        environment: Literal["production", "sandbox"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous llama-stack client instance."""
        self._environment = environment

        base_url_env = os.environ.get("LLAMA_STACK_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `LLAMA_STACK_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.agentic_system = resources.AgenticSystemResource(self)
        self.artifacts = resources.ArtifactsResource(self)
        self.datasets = resources.DatasetsResource(self)
        self.evaluate = resources.EvaluateResource(self)
        self.evaluations = resources.EvaluationsResource(self)
        self.experiments = resources.ExperimentsResource(self)
        self.inference = resources.InferenceResource(self)
        self.logging = resources.LoggingResource(self)
        self.safety = resources.SafetyResource(self)
        self.memory_banks = resources.MemoryBanksResource(self)
        self.post_training = resources.PostTrainingResource(self)
        self.reward_scoring = resources.RewardScoringResource(self)
        self.runs = resources.RunsResource(self)
        self.synthetic_data_generation = resources.SyntheticDataGenerationResource(self)
        self.batch_inference = resources.BatchInferenceResource(self)
        self.with_raw_response = LlamaStackWithRawResponse(self)
        self.with_streaming_response = LlamaStackWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        environment: Literal["production", "sandbox"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncLlamaStack(AsyncAPIClient):
    agentic_system: resources.AsyncAgenticSystemResource
    artifacts: resources.AsyncArtifactsResource
    datasets: resources.AsyncDatasetsResource
    evaluate: resources.AsyncEvaluateResource
    evaluations: resources.AsyncEvaluationsResource
    experiments: resources.AsyncExperimentsResource
    inference: resources.AsyncInferenceResource
    logging: resources.AsyncLoggingResource
    safety: resources.AsyncSafetyResource
    memory_banks: resources.AsyncMemoryBanksResource
    post_training: resources.AsyncPostTrainingResource
    reward_scoring: resources.AsyncRewardScoringResource
    runs: resources.AsyncRunsResource
    synthetic_data_generation: resources.AsyncSyntheticDataGenerationResource
    batch_inference: resources.AsyncBatchInferenceResource
    with_raw_response: AsyncLlamaStackWithRawResponse
    with_streaming_response: AsyncLlamaStackWithStreamedResponse

    # client options

    _environment: Literal["production", "sandbox"] | NotGiven

    def __init__(
        self,
        *,
        environment: Literal["production", "sandbox"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async llama-stack client instance."""
        self._environment = environment

        base_url_env = os.environ.get("LLAMA_STACK_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `LLAMA_STACK_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.agentic_system = resources.AsyncAgenticSystemResource(self)
        self.artifacts = resources.AsyncArtifactsResource(self)
        self.datasets = resources.AsyncDatasetsResource(self)
        self.evaluate = resources.AsyncEvaluateResource(self)
        self.evaluations = resources.AsyncEvaluationsResource(self)
        self.experiments = resources.AsyncExperimentsResource(self)
        self.inference = resources.AsyncInferenceResource(self)
        self.logging = resources.AsyncLoggingResource(self)
        self.safety = resources.AsyncSafetyResource(self)
        self.memory_banks = resources.AsyncMemoryBanksResource(self)
        self.post_training = resources.AsyncPostTrainingResource(self)
        self.reward_scoring = resources.AsyncRewardScoringResource(self)
        self.runs = resources.AsyncRunsResource(self)
        self.synthetic_data_generation = resources.AsyncSyntheticDataGenerationResource(self)
        self.batch_inference = resources.AsyncBatchInferenceResource(self)
        self.with_raw_response = AsyncLlamaStackWithRawResponse(self)
        self.with_streaming_response = AsyncLlamaStackWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        environment: Literal["production", "sandbox"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class LlamaStackWithRawResponse:
    def __init__(self, client: LlamaStack) -> None:
        self.agentic_system = resources.AgenticSystemResourceWithRawResponse(client.agentic_system)
        self.artifacts = resources.ArtifactsResourceWithRawResponse(client.artifacts)
        self.datasets = resources.DatasetsResourceWithRawResponse(client.datasets)
        self.evaluate = resources.EvaluateResourceWithRawResponse(client.evaluate)
        self.evaluations = resources.EvaluationsResourceWithRawResponse(client.evaluations)
        self.experiments = resources.ExperimentsResourceWithRawResponse(client.experiments)
        self.inference = resources.InferenceResourceWithRawResponse(client.inference)
        self.logging = resources.LoggingResourceWithRawResponse(client.logging)
        self.safety = resources.SafetyResourceWithRawResponse(client.safety)
        self.memory_banks = resources.MemoryBanksResourceWithRawResponse(client.memory_banks)
        self.post_training = resources.PostTrainingResourceWithRawResponse(client.post_training)
        self.reward_scoring = resources.RewardScoringResourceWithRawResponse(client.reward_scoring)
        self.runs = resources.RunsResourceWithRawResponse(client.runs)
        self.synthetic_data_generation = resources.SyntheticDataGenerationResourceWithRawResponse(
            client.synthetic_data_generation
        )
        self.batch_inference = resources.BatchInferenceResourceWithRawResponse(client.batch_inference)


class AsyncLlamaStackWithRawResponse:
    def __init__(self, client: AsyncLlamaStack) -> None:
        self.agentic_system = resources.AsyncAgenticSystemResourceWithRawResponse(client.agentic_system)
        self.artifacts = resources.AsyncArtifactsResourceWithRawResponse(client.artifacts)
        self.datasets = resources.AsyncDatasetsResourceWithRawResponse(client.datasets)
        self.evaluate = resources.AsyncEvaluateResourceWithRawResponse(client.evaluate)
        self.evaluations = resources.AsyncEvaluationsResourceWithRawResponse(client.evaluations)
        self.experiments = resources.AsyncExperimentsResourceWithRawResponse(client.experiments)
        self.inference = resources.AsyncInferenceResourceWithRawResponse(client.inference)
        self.logging = resources.AsyncLoggingResourceWithRawResponse(client.logging)
        self.safety = resources.AsyncSafetyResourceWithRawResponse(client.safety)
        self.memory_banks = resources.AsyncMemoryBanksResourceWithRawResponse(client.memory_banks)
        self.post_training = resources.AsyncPostTrainingResourceWithRawResponse(client.post_training)
        self.reward_scoring = resources.AsyncRewardScoringResourceWithRawResponse(client.reward_scoring)
        self.runs = resources.AsyncRunsResourceWithRawResponse(client.runs)
        self.synthetic_data_generation = resources.AsyncSyntheticDataGenerationResourceWithRawResponse(
            client.synthetic_data_generation
        )
        self.batch_inference = resources.AsyncBatchInferenceResourceWithRawResponse(client.batch_inference)


class LlamaStackWithStreamedResponse:
    def __init__(self, client: LlamaStack) -> None:
        self.agentic_system = resources.AgenticSystemResourceWithStreamingResponse(client.agentic_system)
        self.artifacts = resources.ArtifactsResourceWithStreamingResponse(client.artifacts)
        self.datasets = resources.DatasetsResourceWithStreamingResponse(client.datasets)
        self.evaluate = resources.EvaluateResourceWithStreamingResponse(client.evaluate)
        self.evaluations = resources.EvaluationsResourceWithStreamingResponse(client.evaluations)
        self.experiments = resources.ExperimentsResourceWithStreamingResponse(client.experiments)
        self.inference = resources.InferenceResourceWithStreamingResponse(client.inference)
        self.logging = resources.LoggingResourceWithStreamingResponse(client.logging)
        self.safety = resources.SafetyResourceWithStreamingResponse(client.safety)
        self.memory_banks = resources.MemoryBanksResourceWithStreamingResponse(client.memory_banks)
        self.post_training = resources.PostTrainingResourceWithStreamingResponse(client.post_training)
        self.reward_scoring = resources.RewardScoringResourceWithStreamingResponse(client.reward_scoring)
        self.runs = resources.RunsResourceWithStreamingResponse(client.runs)
        self.synthetic_data_generation = resources.SyntheticDataGenerationResourceWithStreamingResponse(
            client.synthetic_data_generation
        )
        self.batch_inference = resources.BatchInferenceResourceWithStreamingResponse(client.batch_inference)


class AsyncLlamaStackWithStreamedResponse:
    def __init__(self, client: AsyncLlamaStack) -> None:
        self.agentic_system = resources.AsyncAgenticSystemResourceWithStreamingResponse(client.agentic_system)
        self.artifacts = resources.AsyncArtifactsResourceWithStreamingResponse(client.artifacts)
        self.datasets = resources.AsyncDatasetsResourceWithStreamingResponse(client.datasets)
        self.evaluate = resources.AsyncEvaluateResourceWithStreamingResponse(client.evaluate)
        self.evaluations = resources.AsyncEvaluationsResourceWithStreamingResponse(client.evaluations)
        self.experiments = resources.AsyncExperimentsResourceWithStreamingResponse(client.experiments)
        self.inference = resources.AsyncInferenceResourceWithStreamingResponse(client.inference)
        self.logging = resources.AsyncLoggingResourceWithStreamingResponse(client.logging)
        self.safety = resources.AsyncSafetyResourceWithStreamingResponse(client.safety)
        self.memory_banks = resources.AsyncMemoryBanksResourceWithStreamingResponse(client.memory_banks)
        self.post_training = resources.AsyncPostTrainingResourceWithStreamingResponse(client.post_training)
        self.reward_scoring = resources.AsyncRewardScoringResourceWithStreamingResponse(client.reward_scoring)
        self.runs = resources.AsyncRunsResourceWithStreamingResponse(client.runs)
        self.synthetic_data_generation = resources.AsyncSyntheticDataGenerationResourceWithStreamingResponse(
            client.synthetic_data_generation
        )
        self.batch_inference = resources.AsyncBatchInferenceResourceWithStreamingResponse(client.batch_inference)


Client = LlamaStack

AsyncClient = AsyncLlamaStack
