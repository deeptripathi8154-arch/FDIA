"""SQLAlchemy ORM models."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DocumentModel(Base):
    """Document table."""

    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    document_type = Column(String(50), default="unknown")
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    error_message = Column(Text, nullable=True)

    def __repr__(self) -> str:
        """String representation."""
        return f"<DocumentModel(id={self.id}, file_name={self.file_name}, status={self.status})>"


class ExtractionModel(Base):
    """Extraction table."""

    __tablename__ = "extractions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id = Column(UUID(as_uuid=True), nullable=False)
    field_name = Column(String(100), nullable=False)
    field_value = Column(Text, nullable=False)
    confidence = Column(Float, default=0.0)
    extracted_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation."""
        return f"<ExtractionModel(id={self.id}, field_name={self.field_name}, confidence={self.confidence})>"
