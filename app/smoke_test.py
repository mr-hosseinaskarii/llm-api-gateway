from __future__ import annotations

import logging

from app.llm_service import (
    LLMConnectionError,
    LLMProviderError,
    LLMRateLimitError,
    LLMService,
    LLMTimeoutError,
)
from app.openai_client import create_openai_client


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    client = create_openai_client()
    service = LLMService(client=client)

    try:
        result = service.generate("API چیست و چه کاری انجام می‌دهد؟")

        print("\n--- MODEL OUTPUT ---")
        print(result.text)

        print("\n--- METADATA ---")
        print(f"model: {result.model}")
        print(f"request_id: {result.request_id}")
        print(f"input_tokens: {result.usage.input_tokens}")
        print(f"output_tokens: {result.usage.output_tokens}")
        print(f"total_tokens: {result.usage.total_tokens}")

    except LLMTimeoutError:
        logger.error("The model request timed out.")

    except LLMRateLimitError:
        logger.error("Rate limit or quota was reached.")

    except LLMConnectionError:
        logger.error("Could not connect to the LLM provider.")

    except LLMProviderError as exc:
        logger.error(
            "LLM provider error status=%s request_id=%s",
            exc.status_code,
            exc.request_id,
        )


if __name__ == "__main__":
    main()