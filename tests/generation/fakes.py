from pydantic import BaseModel

from app.core.exceptions import LLMResponseError
from app.generation.llm_client import SchemaT


class FakeLLMClient:
    """Test double that replays queued responses and records prompts."""

    def __init__(self, responses: list[BaseModel | Exception]) -> None:
        self._responses = list(responses)
        self.prompts: list[str] = []

    def generate_structured(self, prompt: str, schema: type[SchemaT]) -> SchemaT:
        self.prompts.append(prompt)
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        if not isinstance(item, schema):
            raise LLMResponseError("Fake response does not match requested schema")
        return item
