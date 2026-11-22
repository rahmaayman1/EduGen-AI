import re
from collections import Counter

FILLER_DOTS_PATTERN = re.compile(r"\.{4,}")
BIDI_CONTROL_PATTERN = re.compile("[\u200e\u200f\u202a-\u202e\u2066-\u2069\u061c]")
WHITESPACE_RUN_PATTERN = re.compile(r"[ \t]+")
KASHIDA = "\u0640"

MIN_PAGES_FOR_BOILERPLATE_DETECTION = 3
BOILERPLATE_PAGE_RATIO = 0.5


def remove_kashida(text: str) -> str:
    """Remove Arabic tatweel (kashida) characters."""
    return text.replace(KASHIDA, "")


def remove_filler_dots(text: str) -> str:
    """Remove runs of four or more dots used as writing-space fillers."""
    return FILLER_DOTS_PATTERN.sub("", text)


def remove_bidi_marks(text: str) -> str:
    """Remove invisible Unicode bidirectional control characters."""
    return BIDI_CONTROL_PATTERN.sub("", text)


def collapse_whitespace(text: str) -> str:
    """Replace runs of spaces and tabs with a single space."""
    return WHITESPACE_RUN_PATTERN.sub(" ", text)


def clean_text(text: str) -> str:
    """Apply all single-page cleaning steps in a fixed order."""
    text = remove_bidi_marks(text)
    text = remove_kashida(text)
    text = remove_filler_dots(text)
    text = collapse_whitespace(text)
    return text


def remove_repeated_lines(pages: list[str]) -> list[str]:
    """Remove lines that repeat across most pages (headers, footers, ads)."""
    if len(pages) < MIN_PAGES_FOR_BOILERPLATE_DETECTION:
        return pages

    line_page_counts: Counter[str] = Counter()
    for page in pages:
        unique_lines = {line.strip() for line in page.splitlines() if line.strip()}
        line_page_counts.update(unique_lines)

    threshold = len(pages) * BOILERPLATE_PAGE_RATIO
    boilerplate = {
        line for line, count in line_page_counts.items() if count >= threshold
    }

    return [
        "\n".join(line for line in page.splitlines() if line.strip() not in boilerplate)
        for page in pages
    ]
