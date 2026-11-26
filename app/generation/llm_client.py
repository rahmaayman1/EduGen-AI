from typing import Protocol, TypeVar

from pydantic import BaseModel

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class LLMClient(Protocol):
    """Contract for any provider that can return schema-validated output."""

    def generate_structured(self, prompt: str, schema: type[SchemaT]) -> SchemaT:
        """Send a prompt and return the response parsed into schema.

        Raises:
            LLMNotConfiguredError: the provider has no usable credentials.
            LLMUnavailableError: timeout, network failure, or quota exhausted.
            LLMResponseError: the output was empty or did not match the schema.
        """
        ...
