"""Main application entry point.

Enables running the application server via `python -m wordcount`.
"""

import sys
import uvicorn
from wordcount.infrastructure.config import get_settings


def run_server() -> None:
    settings = get_settings()
    print(f"Starting {settings.app_name} v{settings.app_version} on {settings.host}:{settings.port}...")
    uvicorn.run(
        "wordcount.presentation.web.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    run_server()
