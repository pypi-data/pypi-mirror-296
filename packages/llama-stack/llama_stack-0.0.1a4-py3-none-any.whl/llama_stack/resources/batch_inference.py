# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import batch_inference_completion_params, batch_inference_chat_completion_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.batch_chat_completion import BatchChatCompletion
from ..types.shared.batch_completion import BatchCompletion

__all__ = ["BatchInferenceResource", "AsyncBatchInferenceResource"]


class BatchInferenceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BatchInferenceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return BatchInferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BatchInferenceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return BatchInferenceResourceWithStreamingResponse(self)

    def chat_completion(
        self,
        *,
        request: batch_inference_chat_completion_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BatchChatCompletion:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/batch_inference/chat_completion",
            body=maybe_transform(
                {"request": request}, batch_inference_chat_completion_params.BatchInferenceChatCompletionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BatchChatCompletion,
        )

    def completion(
        self,
        *,
        request: batch_inference_completion_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BatchCompletion:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/batch_inference/completion",
            body=maybe_transform(
                {"request": request}, batch_inference_completion_params.BatchInferenceCompletionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BatchCompletion,
        )


class AsyncBatchInferenceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBatchInferenceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBatchInferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBatchInferenceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return AsyncBatchInferenceResourceWithStreamingResponse(self)

    async def chat_completion(
        self,
        *,
        request: batch_inference_chat_completion_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BatchChatCompletion:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/batch_inference/chat_completion",
            body=await async_maybe_transform(
                {"request": request}, batch_inference_chat_completion_params.BatchInferenceChatCompletionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BatchChatCompletion,
        )

    async def completion(
        self,
        *,
        request: batch_inference_completion_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BatchCompletion:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/batch_inference/completion",
            body=await async_maybe_transform(
                {"request": request}, batch_inference_completion_params.BatchInferenceCompletionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BatchCompletion,
        )


class BatchInferenceResourceWithRawResponse:
    def __init__(self, batch_inference: BatchInferenceResource) -> None:
        self._batch_inference = batch_inference

        self.chat_completion = to_raw_response_wrapper(
            batch_inference.chat_completion,
        )
        self.completion = to_raw_response_wrapper(
            batch_inference.completion,
        )


class AsyncBatchInferenceResourceWithRawResponse:
    def __init__(self, batch_inference: AsyncBatchInferenceResource) -> None:
        self._batch_inference = batch_inference

        self.chat_completion = async_to_raw_response_wrapper(
            batch_inference.chat_completion,
        )
        self.completion = async_to_raw_response_wrapper(
            batch_inference.completion,
        )


class BatchInferenceResourceWithStreamingResponse:
    def __init__(self, batch_inference: BatchInferenceResource) -> None:
        self._batch_inference = batch_inference

        self.chat_completion = to_streamed_response_wrapper(
            batch_inference.chat_completion,
        )
        self.completion = to_streamed_response_wrapper(
            batch_inference.completion,
        )


class AsyncBatchInferenceResourceWithStreamingResponse:
    def __init__(self, batch_inference: AsyncBatchInferenceResource) -> None:
        self._batch_inference = batch_inference

        self.chat_completion = async_to_streamed_response_wrapper(
            batch_inference.chat_completion,
        )
        self.completion = async_to_streamed_response_wrapper(
            batch_inference.completion,
        )
