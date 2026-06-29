"""Loguru logger configuration."""

import sys
from pathlib import Path

from loguru import logger

from packages.config import get_settings


def configure_logging() -> None:
    """Configure logging."""
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Create logs directory if it doesn't exist
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Console handler
    logger.add(
        sys.stdout,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
    )

    # File handler
    logger.add(
        settings.log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="500 MB",
        retention="10 days",
    )


def get_logger(name: str = __name__):
    """Get logger instance."""
    configure_logging()
    return logger.bind(name=name)
