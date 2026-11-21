from pathlib import Path

import pymupdf
import pytest

from app.core.exceptions import InvalidPDFError, ScannedDocumentError
from app.documents.service import process_pdf


def create_pdf(path: Path, page_texts: list[str]) -> Path:
    """Create a small PDF where each item in page_texts becomes one page."""
    doc = pymupdf.open()
    for text in page_texts:
        page = doc.new_page()
        if text:
            page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()
    return path


def test_process_pdf_returns_usable_pages(tmp_path: Path) -> None:
    pdf = create_pdf(
        tmp_path / "lesson.pdf",
        ["This is the first page of the lesson about sports.", ""],
    )

    result = process_pdf(pdf)

    assert result.total_pages == 2
    assert result.skipped_pages == 1
    assert len(result.pages) == 1


def test_process_pdf_rejects_non_pdf_file(tmp_path: Path) -> None:
    fake = tmp_path / "fake.pdf"
    fake.write_text("not a pdf")

    with pytest.raises(InvalidPDFError):
        process_pdf(fake)


def test_process_pdf_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(InvalidPDFError):
        process_pdf(tmp_path / "missing.pdf")


def test_process_pdf_rejects_document_without_text(tmp_path: Path) -> None:
    pdf = create_pdf(tmp_path / "scanned.pdf", ["", "", ""])

    with pytest.raises(ScannedDocumentError):
        process_pdf(pdf)
