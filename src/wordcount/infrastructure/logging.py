"""Infrastructure Structured Logging.

Configures standard logging output format and handlers.
"""

from __future__ import annotations
import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Configure system-wide logging with standard timestamped format."""
    log_format = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True
    )
