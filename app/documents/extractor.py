import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pymupdf

MIN_CHARS_FOR_CONTENT = 20
MIN_ARABIC_RATIO = 0.5

ARABIC_LETTER_PATTERN = re.compile(r"[\u0600-\u06FF]")
ANY_LETTER_PATTERN = re.compile(r"[^\W\d_]")


class PageStatus(str, Enum):
    OK = "ok"
    EMPTY = "empty"
    GARBLED = "garbled"


@dataclass(frozen=True)
class PageContent:
    page_number: int
    text: str
    image_count: int
    status: PageStatus


def classify_page_text(text: str) -> PageStatus:
    """Decide whether extracted text is usable, empty, or garbled."""
    stripped = text.strip()
    if len(stripped) < MIN_CHARS_FOR_CONTENT:
        return PageStatus.EMPTY

    arabic_count = len(ARABIC_LETTER_PATTERN.findall(stripped))
    letter_count = len(ANY_LETTER_PATTERN.findall(stripped))
    if letter_count == 0 or arabic_count / letter_count < MIN_ARABIC_RATIO:
        return PageStatus.GARBLED

    return PageStatus.OK


def extract_pages(pdf_path: Path) -> list[PageContent]:
    """Extract text from every page of a PDF and classify each page."""
    pages: list[PageContent] = []
    with pymupdf.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            pages.append(
                PageContent(
                    page_number=page.number + 1,
                    text=text,
                    image_count=len(page.get_images()),
                    status=classify_page_text(text),
                )
            )
    return pages
