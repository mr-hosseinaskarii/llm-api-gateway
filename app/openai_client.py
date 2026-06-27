from __future__ import annotations
import os
from dotenv import load_dotenv
from openai import OpenAI


def create_openai_client() -> OpenAI:
    """Create a configured OpenAI client from environment variables."""

    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing. "
            "Add it to the local .env file and never commit that file."
        )

    return OpenAI(
        timeout=30.0,
        max_retries=2,
    )
