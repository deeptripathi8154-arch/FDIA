"""Phase 1 ingestion and validation primitives for FDIA."""

from packages.ingestion.phase1 import IngestionError, IngestedDocument, ingest_bytes, validate_record

__all__ = ["IngestionError", "IngestedDocument", "ingest_bytes", "validate_record"]
