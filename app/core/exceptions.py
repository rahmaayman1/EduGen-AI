class EduGenError(Exception):
    """Base class for all domain errors raised by the application."""


class InvalidPDFError(EduGenError):
    """Raised when an uploaded file is not a readable PDF."""


class ScannedDocumentError(EduGenError):
    """Raised when a PDF has too little extractable text (likely scanned)."""


class FileTooLargeError(EduGenError):
    """Raised when an uploaded file exceeds the allowed size."""


class LLMError(EduGenError):
    """Base class for failures when calling the language model."""


class LLMNotConfiguredError(LLMError):
    """Raised when the LLM is used but no API key is configured."""


class LLMUnavailableError(LLMError):
    """Raised on timeouts, network failures, or exhausted quota."""


class LLMResponseError(LLMError):
    """Raised when the model returns output that is empty or invalid."""
