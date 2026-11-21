from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    total_pages: int
    skipped_pages: int
