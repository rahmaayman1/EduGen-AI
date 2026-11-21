import io
from pathlib import Path

import pytest

from app.core.exceptions import FileTooLargeError, InvalidPDFError
from app.documents.storage import save_pdf_upload

VALID_PDF_BYTES = b"%PDF-1.4 fake content"


def test_save_pdf_upload_stores_file_with_random_name(tmp_path: Path) -> None:
    saved = save_pdf_upload(io.BytesIO(VALID_PDF_BYTES), tmp_path, max_bytes=1000)

    assert saved.parent == tmp_path
    assert saved.suffix == ".pdf"
    assert saved.read_bytes() == VALID_PDF_BYTES


def test_save_pdf_upload_rejects_non_pdf_content(tmp_path: Path) -> None:
    with pytest.raises(InvalidPDFError):
        save_pdf_upload(io.BytesIO(b"hello world"), tmp_path, max_bytes=1000)

    assert list(tmp_path.iterdir()) == []


def test_save_pdf_upload_rejects_oversized_file_and_cleans_up(tmp_path: Path) -> None:
    big = io.BytesIO(VALID_PDF_BYTES + b"x" * 2000)

    with pytest.raises(FileTooLargeError):
        save_pdf_upload(big, tmp_path, max_bytes=1000)

    assert list(tmp_path.iterdir()) == []
