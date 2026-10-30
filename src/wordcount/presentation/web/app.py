"""FastAPI Application Factory.

Constructs and configures the ASGI web application instance with middleware,
static files, routers, and lifecycle events.
"""

from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from wordcount.infrastructure.config import Settings, get_settings
from wordcount.infrastructure.logging import setup_logging
from wordcount.presentation.web.routes import api_router, web_router

STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""
    if settings is None:
        settings = get_settings()

    setup_logging(level=settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Enterprise-grade Text Analysis & Linguistic Metrics Engine. "
            "Built with Keystone Clean Architecture principles."
        ),
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Static Assets
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    # Register Routers
    app.include_router(web_router)
    app.include_router(api_router)

    return app


app = create_app()
