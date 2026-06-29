"""Document domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Document:
    """Finance document entity."""

    id: UUID = field(default_factory=uuid4)
    file_name: str = ""
    file_path: str = ""
    file_size: int = 0
    document_type: str = ""  # invoice, receipt, etc.
    status: str = "pending"  # pending, processing, completed, failed
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    error_message: str = ""

    class Meta:
        """Document metadata."""

        table_name = "documents"
