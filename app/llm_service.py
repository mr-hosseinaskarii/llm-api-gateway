from __future__ import annotations

import os
from dataclasses import dataclass

import openai
from openai import OpenAI


DEFAULT_INSTRUCTIONS = (
    "You are a concise technical tutor. "
    "Answer in Persian and do not exceed two sentences."
)


@dataclass(frozen=True)
class LLMUsage:
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None


@dataclass(frozen=True)
class LLMResult:
    text: str
    model: str
    request_id: str | None
    usage: LLMUsage


class LLMServiceError(RuntimeError):
    """Base error for LLM service failures."""


class LLMTimeoutError(LLMServiceError):
    """Raised when the LLM provider request times out."""


class LLMRateLimitError(LLMServiceError):
    """Raised when the LLM provider rate limit or quota is reached."""


class LLMConnectionError(LLMServiceError):
    """Raised when the application cannot connect to the LLM provider."""


class LLMProviderError(LLMServiceError):
    """Raised when the LLM provider returns an API status error."""

    def __init__(self, message: str, status_code: int | None, request_id: str | None):
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id


class LLMService:
    def __init__(self, client: OpenAI, model: str | None = None) -> None:
        self.client = client
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.4-mini-2026-03-17")

    def generate(
        self,
        user_input: str,
        instructions: str = DEFAULT_INSTRUCTIONS,
        max_output_tokens: int = 120,
    ) -> LLMResult:
        if not user_input.strip():
            raise ValueError("user_input must not be empty.")

        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=instructions,
                input=user_input,
                max_output_tokens=max_output_tokens,
            )

        except openai.APITimeoutError as exc:
            raise LLMTimeoutError("The model request timed out.") from exc

        except openai.RateLimitError as exc:
            raise LLMRateLimitError("Rate limit or quota was reached.") from exc

        except openai.APIConnectionError as exc:
            raise LLMConnectionError("Could not connect to the LLM provider.") from exc

        except openai.APIStatusError as exc:
            raise LLMProviderError(
                message="The LLM provider returned an API error.",
                status_code=exc.status_code,
                request_id=exc.request_id,
            ) from exc

        usage = response.usage

        return LLMResult(
            text=response.output_text,
            model=response.model,
            request_id=response._request_id,
            usage=LLMUsage(
                input_tokens=usage.input_tokens if usage else None,
                output_tokens=usage.output_tokens if usage else None,
                total_tokens=usage.total_tokens if usage else None,
            ),
        )
