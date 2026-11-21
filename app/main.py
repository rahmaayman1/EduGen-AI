from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import Settings, get_settings
from app.core.exceptions import (
    EduGenError,
    FileTooLargeError,
    InvalidPDFError,
    ScannedDocumentError,
)
from app.documents.router import router as documents_router

# --- Constants ---

ERROR_STATUS_CODES: dict[type[EduGenError], int] = {
    InvalidPDFError: 422,
    ScannedDocumentError: 422,
    FileTooLargeError: 413,
}

# --- App creation ---

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

# --- Exception handlers ---


@app.exception_handler(EduGenError)
async def handle_domain_error(request: Request, exc: EduGenError) -> JSONResponse:
    status_code = ERROR_STATUS_CODES.get(type(exc), 400)
    return JSONResponse(
        status_code=status_code,
        content={"error": type(exc).__name__, "message": str(exc)},
    )


# --- Routers ---

app.include_router(documents_router)

# --- Direct endpoints ---


@app.get("/health")
def health_check(
    current_settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str]:
    """Report that the service is up, along with basic environment info."""
    return {
        "status": "ok",
        "app": current_settings.app_name,
        "environment": current_settings.environment,
    }
