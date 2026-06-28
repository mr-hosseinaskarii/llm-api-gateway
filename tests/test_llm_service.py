from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.llm_service import LLMService


def test_generate_rejects_empty_user_input() -> None:
    fake_client = SimpleNamespace()
    service = LLMService(client=fake_client, model="test-model")

    with pytest.raises(ValueError, match="user_input must not be empty"):
        service.generate("   ")


def test_generate_returns_normalized_llm_result() -> None:
    captured_request: dict[str, object] = {}

    def fake_create(**kwargs: object) -> SimpleNamespace:
        captured_request.update(kwargs)

        return SimpleNamespace(
            output_text="پاسخ تستی",
            model="test-model-snapshot",
            _request_id="req_test_123",
            usage=SimpleNamespace(
                input_tokens=10,
                output_tokens=5,
                total_tokens=15,
            ),
        )

    fake_client = SimpleNamespace(
        responses=SimpleNamespace(
            create=fake_create,
        )
    )

    service = LLMService(client=fake_client, model="test-model")
    result = service.generate(
        user_input="API چیست؟",
        instructions="Answer briefly.",
        max_output_tokens=50,
    )

    assert captured_request == {
        "model": "test-model",
        "instructions": "Answer briefly.",
        "input": "API چیست؟",
        "max_output_tokens": 50,
    }

    assert result.text == "پاسخ تستی"
    assert result.model == "test-model-snapshot"
    assert result.request_id == "req_test_123"
    assert result.usage.input_tokens == 10
    assert result.usage.output_tokens == 5
    assert result.usage.total_tokens == 15