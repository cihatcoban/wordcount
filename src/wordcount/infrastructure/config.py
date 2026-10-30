"""Infrastructure Configuration.

Implements Twelve-Factor App principles using environment variables
with strongly typed defaults and validation.
"""

from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Settings:
    """Application and server configuration settings."""
    app_name: str = "WordCount Pro"
    app_version: str = "2.0.0"
    environment: str = field(
        default_factory=lambda: os.getenv("APP_ENV", "production")
    )
    debug: bool = field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    )
    host: str = field(
        default_factory=lambda: os.getenv("HOST", "127.0.0.1")
    )
    port: int = field(
        default_factory=lambda: int(os.getenv("PORT", "8000"))
    )
    max_text_length: int = field(
        default_factory=lambda: int(os.getenv("MAX_TEXT_LENGTH", "2000000"))
    )
    allowed_origins: List[str] = field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
            if origin.strip()
        ]
    )
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper()
    )


def get_settings() -> Settings:
    """Factory helper to obtain cached or fresh application settings."""
    return Settings()
