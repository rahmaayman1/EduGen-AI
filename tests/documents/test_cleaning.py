import pytest

from app.documents.cleaning import remove_filler_dots, remove_kashida


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
