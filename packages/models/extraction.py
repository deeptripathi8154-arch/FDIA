"""Extraction domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Extraction:
    """Extracted fields from document."""

    id: UUID = field(default_factory=uuid4)
    document_id: UUID = field(default_factory=uuid4)
    field_name: str = ""
    field_value: str = ""
    confidence: float = 0.0
    extracted_at: datetime = field(default_factory=datetime.utcnow)

    class Meta:
        """Extraction metadata."""

        table_name = "extractions"
