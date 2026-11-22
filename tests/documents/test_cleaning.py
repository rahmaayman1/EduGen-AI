import pytest

from app.documents.cleaning import (
    clean_text,
    collapse_whitespace,
    remove_bidi_marks,
    remove_filler_dots,
    remove_kashida,
    remove_repeated_lines,
)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("رياضـة", "رياضة"),
        ("مـــرحبـــا", "مرحبا"),
        ("بدون تطويل", "بدون تطويل"),
        ("", ""),
    ],
)
def test_remove_kashida(text: str, expected: str) -> None:
    assert remove_kashida(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("عنوان القصة ..........", "عنوان القصة "),
        ("a....b", "ab"),
        ("نقاط حذف ... عادية", "نقاط حذف ... عادية"),
        ("جملة منتهية.", "جملة منتهية."),
    ],
)
def test_remove_filler_dots(text: str, expected: str) -> None:
    assert remove_filler_dots(text) == expected


def test_clean_text_applies_all_steps() -> None:
    raw = "رياضـة\u200f   عنوان ..........  نهاية"
    assert clean_text(raw) == "رياضة عنوان نهاية"


def test_remove_repeated_lines_removes_boilerplate() -> None:
    pages = [
        "إعلان القناة\nدرس الصفحة الأولى",
        "إعلان القناة\nدرس الصفحة الثانية",
        "إعلان القناة\nدرس الصفحة الثالثة",
    ]

    result = remove_repeated_lines(pages)

    assert result == [
        "درس الصفحة الأولى",
        "درس الصفحة الثانية",
        "درس الصفحة الثالثة",
    ]


def test_remove_repeated_lines_keeps_unique_content() -> None:
    pages = ["سطر أول", "سطر ثاني", "سطر ثالث"]
    assert remove_repeated_lines(pages) == pages


def test_remove_repeated_lines_skips_short_documents() -> None:
    pages = ["نفس السطر", "نفس السطر"]
    assert remove_repeated_lines(pages) == pages


@pytest.mark.parametrize(
    "text, expected",
    [
        ("مرحبا\u200f بالعالم", "مرحبا بالعالم"),
        ("\u202bنص\u202c", "نص"),
        ("نص عادي", "نص عادي"),
    ],
)
def test_remove_bidi_marks(text: str, expected: str) -> None:
    assert remove_bidi_marks(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("كلمة    كلمة", "كلمة كلمة"),
        ("a\t\tb", "a b"),
        ("سطر\nسطر", "سطر\nسطر"),
    ],
)
def test_collapse_whitespace(text: str, expected: str) -> None:
    assert collapse_whitespace(text) == expected
