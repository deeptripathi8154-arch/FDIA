"""Data access layer."""

from .base import BaseRepository
from .document_repository import DocumentRepository
from .extraction_repository import ExtractionRepository

__all__ = [
    "BaseRepository",
    "DocumentRepository",
    "ExtractionRepository",
]
