from app.documents.chunking import chunk_pages, split_into_units
from app.documents.extractor import PageContent, PageStatus


def make_page(number: int, text: str) -> PageContent:
    return PageContent(
        page_number=number, text=text, image_count=0, status=PageStatus.OK
    )


def test_short_text_becomes_single_chunk() -> None:
    chunks = chunk_pages([make_page(1, "سطر أول\nسطر ثاني")])

    assert len(chunks) == 1
    assert chunks[0].text == "سطر أول\nسطر ثاني"
    assert (chunks[0].page_start, chunks[0].page_end) == (1, 1)


def test_text_is_split_when_limit_exceeded() -> None:
    page = make_page(1, "aaaaaaaaaa\nbbbbbbbbbb\ncccccccccc")

    chunks = chunk_pages([page], max_chars=25)

    assert [c.text for c in chunks] == ["aaaaaaaaaa\nbbbbbbbbbb", "cccccccccc"]
    assert [c.index for c in chunks] == [0, 1]


def test_chunk_tracks_page_range() -> None:
    pages = [make_page(1, "سطر من الصفحة الأولى"), make_page(2, "سطر من الثانية")]

    chunks = chunk_pages(pages)

    assert len(chunks) == 1
    assert (chunks[0].page_start, chunks[0].page_end) == (1, 2)


def test_empty_pages_produce_no_chunks() -> None:
    assert chunk_pages([make_page(1, ""), make_page(2, "  \n \n")]) == []


def test_long_line_is_split_at_sentence_boundaries() -> None:
    line = "الجملة الأولى هنا. الجملة الثانية هنا؟ الجملة الثالثة هنا!"
    assert split_into_units(line, max_chars=30) == [
        "الجملة الأولى هنا.",
        "الجملة الثانية هنا؟",
        "الجملة الثالثة هنا!",
    ]


def test_short_line_is_not_split() -> None:
    assert split_into_units("جملة. وجملة تانية.", max_chars=100) == [
        "جملة. وجملة تانية."
    ]
