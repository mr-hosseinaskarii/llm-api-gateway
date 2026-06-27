from __future__ import annotations
import logging
import os
import openai
from app.openai_client import create_openai_client


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    client = create_openai_client()
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

    try:
        response = client.responses.create(
            model=model,
            instructions=(
                "You are a concise technical tutor. "
                "Answer in Persian and do not exceed two sentences."
            ),
            input="API چیست و چه کاری انجام می‌دهد؟",
            max_output_tokens=120,
        )

        print("\n--- MODEL OUTPUT ---")
        print(response.output_text)

        print("\n--- METADATA ---")
        print(f"model: {response.model}")
        print(f"request_id: {response._request_id}")

        if response.usage:
            print(f"input_tokens: {response.usage.input_tokens}")
            print(f"output_tokens: {response.usage.output_tokens}")
            print(f"total_tokens: {response.usage.total_tokens}")

    except openai.APITimeoutError:
        logger.error("The model request timed out.")

    except openai.RateLimitError:
        logger.error("Rate limit or quota was reached.")

    except openai.APIConnectionError as exc:
        logger.error("Could not connect to the OpenAI API: %s", exc)

    except openai.APIStatusError as exc:
        logger.error(
            "OpenAI returned status=%s request_id=%s",
            exc.status_code,
            exc.request_id,
        )


if __name__ == "__main__":
    main()