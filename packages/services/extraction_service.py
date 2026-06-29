"""Extraction service - business logic."""

from typing import List, Optional
from uuid import UUID

from packages.logging import get_logger
from packages.models import Extraction, ExtractionStatus
from packages.repositories import ExtractionRepository

logger = get_logger(__name__)


class ExtractionService:
    """Extraction business logic."""

    def __init__(self, repository: ExtractionRepository) -> None:
        """Initialize service."""
        self.repository = repository

    def extract_field(
        self,
        document_id: UUID,
        field_name: str,
        field_value: str,
        confidence: float = 0.0,
    ) -> Extraction:
        """Extract field from document.
        
        Args:
            document_id: Document ID
            field_name: Name of the field
            field_value: Extracted value
            confidence: Confidence score
            
        Returns:
            Created extraction
        """
        logger.info(f"Extracting field: {field_name} from document: {document_id}")
        
        extraction = Extraction(
            document_id=document_id,
            field_name=field_name,
            field_value=field_value,
            confidence=confidence,
        )
        
        return self.repository.create(extraction)

    def get_extractions(self, document_id: UUID) -> List[Extraction]:
        """Get all extractions for a document.
        
        Args:
            document_id: Document ID
            
        Returns:
            List of extractions
        """
        return self.repository.list_by_document(document_id)

    def get_extraction_confidence(
        self, document_id: UUID
    ) -> Optional[float]:
        """Get average confidence for a document.
        
        Args:
            document_id: Document ID
            
        Returns:
            Average confidence or None
        """
        extractions = self.get_extractions(document_id)
        if not extractions:
            return None
        
        avg_confidence = sum(e.confidence for e in extractions) / len(extractions)
        return avg_confidence
