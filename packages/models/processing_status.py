"""Processing status enums."""

from enum import Enum


class DocumentStatus(str, Enum):
    """Document processing status."""

    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    OCR = "ocr"
    EXTRACTION = "extraction"
    VALIDATION = "validation"
    COMPLETED = "completed"
    FAILED = "failed"


class ExtractionStatus(str, Enum):
    """Extraction status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
