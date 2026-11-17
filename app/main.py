from typing import Annotated
from fastapi import Depends, FastAPI
from app.core.config import get_settings, Settings

settings = get_settings()

app = FastAPI(title = settings.app_name, debug = settings.debug)

@app.get("/health")
def health_check(
    current_settings: Annotated[Settings, Depends(get_settings)],
) ->dict[str,str]:
    """Report that the service is up, along with basic environment info."""
    return {
        "status": "ok",
        "app": current_settings.app_name,
        "environment": current_settings.environment,
    }