class EduGenError(Exception):
    """Base class for all domain errors raised by the application."""


class InvalidPDFError(EduGenError):
    """Raised when an uploaded file is not a readable PDF."""


class ScannedDocumentError(EduGenError):
    """Raised when a PDF has too little extractable text (likely scanned)."""


class FileTooLargeError(EduGenError):
    """Raised when an uploaded file exceeds the allowed size."""
