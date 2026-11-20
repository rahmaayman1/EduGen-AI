import uuid
from pathlib import Path
from typing import BinaryIO

from app.core.exceptions import FileTooLargeError, InvalidPDFError

PDF_MAGIC_BYTES = b"%PDF-"
CHUNK_SIZE = 1024 * 1024


def save_pdf_upload(source: BinaryIO, storage_dir: Path, max_bytes: int) -> Path:
    """Validate and save an uploaded PDF under a random name; return its path."""
    header = source.read(len(PDF_MAGIC_BYTES))
    if header != PDF_MAGIC_BYTES:
        raise InvalidPDFError("File content is not a PDF")

    storage_dir.mkdir(parents=True, exist_ok=True)
    destination = storage_dir / f"{uuid.uuid4().hex}.pdf"
    total_bytes = len(header)

    try:
        with destination.open("wb") as out:
            out.write(header)
            while chunk := source.read(CHUNK_SIZE):
                total_bytes += len(chunk)
                if total_bytes > max_bytes:
                    raise FileTooLargeError(f"File exceeds {max_bytes} bytes")
                out.write(chunk)
    except FileTooLargeError:
        destination.unlink(missing_ok=True)
        raise

    return destination
