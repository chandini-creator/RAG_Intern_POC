"""
Centralized logging setup.
Uses level from config; logs to stdout for container/cloud-friendly output.
"""
import logging
import sys
from typing import Optional

from app.config import get_settings


def setup_logging(level: Optional[str] = None) -> None:
    """Configure root logger and uvicorn log level."""
    settings = get_settings()
    log_level = (level or settings.log_level).upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Avoid duplicate logs from uvicorn
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
