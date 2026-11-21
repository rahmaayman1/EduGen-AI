import re

FILLER_DOTS_PATTERN = re.compile(r"\.{4,}")
KASHIDA = "\u0640"


def remove_kashida(text: str) -> str:
    """Remove Arabic tatweel (kashida) characters."""
    return text.replace(KASHIDA, "")


def remove_filler_dots(text: str) -> str:
    """Remove runs of four or more dots used as writing-space fillers."""
    return FILLER_DOTS_PATTERN.sub("", text)
