import re
from dataclasses import dataclass

from app.documents.extractor import PageContent

SENTENCE_BOUNDARY_PATTERN = re.compile(r"(?<=[.!?؟؛])\s+")

MAX_CHUNK_CHARS = 3000


@dataclass(frozen=True)
class Chunk:
    index: int
    text: str
    page_start: int
    page_end: int


def split_into_units(text: str, max_chars: int) -> list[str]:
    """Split text into lines; break oversized lines into sentences."""
    units: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if len(line) <= max_chars:
            units.append(line)
        else:
            units.extend(s for s in SENTENCE_BOUNDARY_PATTERN.split(line) if s)
    return units


def chunk_pages(
    pages: list[PageContent], max_chars: int = MAX_CHUNK_CHARS
) -> list[Chunk]:
    """Group page paragraphs into chunks of at most max_chars characters."""
    chunks: list[Chunk] = []
    buffer: list[str] = []
    buffer_length = 0
    start_page = 0
    end_page = 0

    def flush() -> None:
        nonlocal buffer, buffer_length
        if buffer:
            chunks.append(
                Chunk(
                    index=len(chunks),
                    text="\n".join(buffer),
                    page_start=start_page,
                    page_end=end_page,
                )
            )
        buffer = []
        buffer_length = 0

    for page in pages:
        for paragraph in split_into_units(page.text, max_chars):
            if buffer and buffer_length + len(paragraph) > max_chars:
                flush()
            if not buffer:
                start_page = page.page_number
            buffer.append(paragraph)
            buffer_length += len(paragraph) + 1
            end_page = page.page_number

    flush()
    return chunks
