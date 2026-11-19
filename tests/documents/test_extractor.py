import pytest

from app.documents.extractor import (
    MIN_CHARS_FOR_CONTENT,
    PageStatus,
    classify_page_text,
)

ARABIC_SENTENCE = "هذا درس عن الرياضة والحياة الصحية للطلاب"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", PageStatus.EMPTY),
        ("   \n\t  ", PageStatus.EMPTY),
        ("1", PageStatus.EMPTY),
        ("ا" * (MIN_CHARS_FOR_CONTENT - 1), PageStatus.EMPTY),
        ("ا" * MIN_CHARS_FOR_CONTENT, PageStatus.OK),
        (ARABIC_SENTENCE, PageStatus.OK),
        ("这是一个关于体育的课程内容测试文本" * 3, PageStatus.GARBLED),
        ("This is a lesson about sports and health", PageStatus.GARBLED),
        ("12345 67890 12345 67890 12345 67890", PageStatus.GARBLED),
    ],
)
def test_classify_page_text(text: str, expected: PageStatus) -> None:
    assert classify_page_text(text) == expected


def test_arabic_text_with_numbers_and_punctuation_is_ok() -> None:
    text = f"{ARABIC_SENTENCE} 123 ... !!! (2024)"
    assert classify_page_text(text) == PageStatus.OK
