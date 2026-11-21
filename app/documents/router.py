from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from app.core.config import Settings, get_settings
from app.core.exceptions import EduGenError
from app.documents.schemas import DocumentUploadResponse
from app.documents.service import process_pdf
from app.documents.storage import save_pdf_upload

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("", status_code=201)
def upload_document(
    file: UploadFile,
    settings: Annotated[Settings, Depends(get_settings)],
) -> DocumentUploadResponse:
    """Upload a PDF lesson, validate it, and report extraction results."""
    saved_path: Path = save_pdf_upload(
        file.file, settings.storage_dir, settings.max_upload_size_bytes
    )
    try:
        extracted = process_pdf(saved_path)
    except EduGenError:
        saved_path.unlink(missing_ok=True)
        raise

    return DocumentUploadResponse(
        document_id=saved_path.stem,
        total_pages=extracted.total_pages,
        skipped_pages=extracted.skipped_pages,
    )
