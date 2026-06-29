"""Document service - business logic."""

from typing import List, Optional
from uuid import UUID

from packages.logging import get_logger
from packages.models import Document, DocumentStatus
from packages.repositories import DocumentRepository

logger = get_logger(__name__)


class DocumentService:
    """Document business logic."""

    def __init__(self, repository: DocumentRepository) -> None:
        """Initialize service."""
        self.repository = repository

    def create_document(
        self, file_name: str, file_path: str, document_type: str
    ) -> Document:
        """Create new document.
        
        Args:
            file_name: Name of the file
            file_path: Path to the file
            document_type: Type of document
            
        Returns:
            Created document
        """
        logger.info(f"Creating document: {file_name}")
        
        doc = Document(
            file_name=file_name,
            file_path=file_path,
            document_type=document_type,
            status=DocumentStatus.PENDING.value,
        )
        
        return self.repository.create(doc)

    def get_document(self, document_id: UUID) -> Optional[Document]:
        """Get document by ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            Document or None
        """
        return self.repository.read(document_id)

    def list_pending_documents(self) -> List[Document]:
        """List pending documents.
        
        Returns:
            List of pending documents
        """
        return self.repository.list_by_status(DocumentStatus.PENDING.value)

    def mark_processing(self, document_id: UUID) -> Optional[Document]:
        """Mark document as processing.
        
        Args:
            document_id: Document ID
            
        Returns:
            Updated document or None
        """
        doc = self.repository.read(document_id)
        if doc:
            doc.status = DocumentStatus.PROCESSING.value
            return self.repository.update(doc)
        return None

    def mark_completed(self, document_id: UUID) -> Optional[Document]:
        """Mark document as completed.
        
        Args:
            document_id: Document ID
            
        Returns:
            Updated document or None
        """
        doc = self.repository.read(document_id)
        if doc:
            doc.status = DocumentStatus.COMPLETED.value
            return self.repository.update(doc)
        return None

    def mark_failed(self, document_id: UUID, error_message: str) -> Optional[Document]:
        """Mark document as failed.
        
        Args:
            document_id: Document ID
            error_message: Error message
            
        Returns:
            Updated document or None
        """
        doc = self.repository.read(document_id)
        if doc:
            doc.status = DocumentStatus.FAILED.value
            doc.error_message = error_message
            return self.repository.update(doc)
        return None
