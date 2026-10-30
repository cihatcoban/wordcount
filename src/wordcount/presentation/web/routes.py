"""FastAPI Web & REST API Route Definitions.

Exposes RESTful endpoints for programmatic access and renders the HTML dashboard.
"""

from __future__ import annotations
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from wordcount.application.dtos import AnalyzeTextCommand, TextAnalysisResultDTO
from wordcount.application.use_cases import AnalyzeTextUseCase
from wordcount.infrastructure.config import Settings, get_settings

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

api_router = APIRouter(prefix="/api/v1", tags=["Analysis"])
web_router = APIRouter(tags=["Web UI"])


class AnalyzeRequest(BaseModel):
    """Schema for text analysis payload."""
    text: str = Field(..., description="The raw input text to analyze")
    top_n_keywords: int = Field(default=10, ge=1, le=100, description="Number of top frequent keywords to return")
    filter_stopwords: bool = Field(default=False, description="Filter common grammatical stopwords")

    class Config:
        schema_extra = {
            "example": {
                "text": "Keystone architecture emphasizes clean boundaries and test-driven domain logic.",
                "top_n_keywords": 5,
                "filter_stopwords": True
            }
        }


def get_use_case(settings: Settings = Depends(get_settings)) -> AnalyzeTextUseCase:
    """Dependency injection provider for AnalyzeTextUseCase."""
    return AnalyzeTextUseCase(max_text_length=settings.max_text_length)


@web_router.get("/", response_class=HTMLResponse)
async def render_dashboard(
    request: Request,
    settings: Settings = Depends(get_settings)
) -> HTMLResponse:
    """Render interactive web application interface."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "version": settings.app_version,
            "max_chars": settings.max_text_length,
        }
    )


@api_router.get("/health")
async def health_check(settings: Settings = Depends(get_settings)) -> Dict[str, Any]:
    """Liveness and health status probe."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }


@api_router.post("/analyze", response_model=Dict[str, Any])
async def analyze_text_endpoint(
    payload: AnalyzeRequest,
    use_case: AnalyzeTextUseCase = Depends(get_use_case)
) -> Dict[str, Any]:
    """Execute deep linguistic and readability analysis on submitted text."""
    try:
        command = AnalyzeTextCommand(
            text=payload.text,
            top_n_keywords=payload.top_n_keywords,
            filter_stopwords=payload.filter_stopwords
        )
        result: TextAnalysisResultDTO = use_case.execute(command)
        return result.to_dict()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(exc)}")
