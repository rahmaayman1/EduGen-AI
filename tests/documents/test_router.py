from collections.abc import Iterator
from pathlib import Path

import pymupdf
import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app

MAX_BYTES_MB = 1


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    app.dependency_overrides[get_settings] = lambda: Settings(
        storage_dir=tmp_path, max_upload_size_mb=MAX_BYTES_MB
    )
    yield TestClient(app)
    app.dependency_overrides.clear()


def make_pdf_bytes(page_texts: list[str]) -> bytes:
    doc = pymupdf.open()
    for text in page_texts:
        page = doc.new_page()
        if text:
            page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data


def test_upload_valid_pdf_returns_201(client: TestClient, tmp_path: Path) -> None:
    pdf = make_pdf_bytes(["This is a lesson page about sports and health."])

    response = client.post(
        "/api/v1/documents", files={"file": ("lesson.pdf", pdf, "application/pdf")}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["total_pages"] == 1
    assert (tmp_path / f"{body['document_id']}.pdf").exists()


def test_upload_non_pdf_returns_422_and_stores_nothing(
    client: TestClient, tmp_path: Path
) -> None:
    response = client.post(
        "/api/v1/documents", files={"file": ("fake.pdf", b"hello", "application/pdf")}
    )

    assert response.status_code == 422
    assert response.json()["error"] == "InvalidPDFError"
    assert list(tmp_path.iterdir()) == []


def test_upload_scanned_pdf_returns_422_and_deletes_file(
    client: TestClient, tmp_path: Path
) -> None:
    pdf = make_pdf_bytes(["", "", ""])

    response = client.post(
        "/api/v1/documents", files={"file": ("scan.pdf", pdf, "application/pdf")}
    )

    assert response.status_code == 422
    assert response.json()["error"] == "ScannedDocumentError"
    assert list(tmp_path.iterdir()) == []


def test_upload_oversized_file_returns_413(client: TestClient, tmp_path: Path) -> None:
    too_big = b"%PDF-" + b"x" * (MAX_BYTES_MB * 1024 * 1024 + 1)

    response = client.post(
        "/api/v1/documents", files={"file": ("big.pdf", too_big, "application/pdf")}
    )

    assert response.status_code == 413
    assert list(tmp_path.iterdir()) == []
