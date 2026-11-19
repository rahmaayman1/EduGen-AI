import sys

import pymupdf


def probe_pdf(path: str, preview_chars: int = 400) -> None:
    """Print basic extraction diagnostics for each page of a PDF."""
    with pymupdf.open(path) as doc:
        print(f"File: {path}")
        print(f"Pages: {doc.page_count}\n")

        for page in doc:
            text = page.get_text()
            images = page.get_images()
            print(f"--- Page {page.number + 1} ---")
            print(f"Characters: {len(text.strip())} | Images: {len(images)}")
            print(text[:preview_chars])
            print()


if __name__ == "__main__":
    probe_pdf(sys.argv[1])
