"""Custom application exceptions."""


class ApplicationException(Exception):
    """Base application exception."""

    def __init__(self, message: str, code: str = "ERROR") -> None:
        """Initialize exception."""
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationException(ApplicationException):
    """Validation error."""

    def __init__(self, message: str) -> None:
        """Initialize exception."""
        super().__init__(message, "VALIDATION_ERROR")


class DatabaseException(ApplicationException):
    """Database error."""

    def __init__(self, message: str) -> None:
        """Initialize exception."""
        super().__init__(message, "DATABASE_ERROR")


class OcrException(ApplicationException):
    """OCR processing error."""

    def __init__(self, message: str) -> None:
        """Initialize exception."""
        super().__init__(message, "OCR_ERROR")


class ExtractionException(ApplicationException):
    """AI extraction error."""

    def __init__(self, message: str) -> None:
        """Initialize exception."""
        super().__init__(message, "EXTRACTION_ERROR")
