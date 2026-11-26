import pytest
from pydantic import BaseModel

from app.core.exceptions import LLMResponseError, LLMUnavailableError
from tests.generation.fakes import FakeLLMClient


class Sample(BaseModel):
    answer: str


def test_fake_returns_queued_response_and_records_prompt() -> None:
    client = FakeLLMClient([Sample(answer="42")])

    result = client.generate_structured("question?", Sample)

    assert result.answer == "42"
    assert client.prompts == ["question?"]


def test_fake_raises_queued_error() -> None:
    client = FakeLLMClient([LLMUnavailableError("timeout")])

    with pytest.raises(LLMUnavailableError):
        client.generate_structured("question?", Sample)


def test_fake_rejects_wrong_schema() -> None:
    class Other(BaseModel):
        value: int

    client = FakeLLMClient([Sample(answer="x")])

    with pytest.raises(LLMResponseError):
        client.generate_structured("question?", Other)
