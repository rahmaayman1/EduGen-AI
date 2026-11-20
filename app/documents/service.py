from dataclasses import dataclass
from pathlib import Path

import pymupdf

from app.core.exceptions import InvalidPDFError, ScannedDocumentError
from app.documents.extractor import PageContent, PageStatus, extract_pages

MIN_OK_PAGES_RATIO = 0.5


@dataclass(frozen=True)
class ExtractedDocument:
    pages: list[PageContent]
    total_pages: int
    skipped_pages: int


def process_pdf(pdf_path: Path) -> ExtractedDocument:
    """Extract usable text from a PDF or raise a domain error if it is unusable."""
    try:
        all_pages = extract_pages(pdf_path)
    except (pymupdf.FileDataError, pymupdf.EmptyFileError, pymupdf.FileNotFoundError) as exc:
        raise InvalidPDFError(f"Could not read PDF: {pdf_path.name}") from exc

    if not all_pages:
        raise InvalidPDFError("PDF has no pages")

    usable_pages = [p for p in all_pages if p.status == PageStatus.OK]
    ok_ratio = len(usable_pages) / len(all_pages)

    if ok_ratio < MIN_OK_PAGES_RATIO:
        raise ScannedDocumentError(
            f"Only {len(usable_pages)} of {len(all_pages)} pages contain readable text"
        )

    return ExtractedDocument(
        pages=usable_pages,
        total_pages=len(all_pages),
        skipped_pages=len(all_pages) - len(usable_pages),
    )
