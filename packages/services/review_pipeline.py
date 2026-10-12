"""Connect ingested documents to normalized records and the local review queue."""
from __future__ import annotations

import re
from typing import Any

from packages.ingestion.phase1 import IngestedDocument
from packages.review.workflow import ReviewQueue, ReviewRecord, build_review_record


def _labelled_values(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*([^:=]{1,80})\s*[:=]\s*(.*?)\s*$", line)
        if match and match.group(2):
            values[match.group(1).strip()] = match.group(2).strip()
    return values


def enqueue_document(document: IngestedDocument, workflow: str, queue: ReviewQueue) -> list[ReviewRecord]:
    """Create pending review records from structured rows or labelled text.

    This is deterministic field mapping, not an LLM guess. Unmapped values remain
    visible on the record. Documents with no recognizable fields fail closed.
    """
    source_records: list[dict[str, Any]] = list(document.rows)
    if not source_records and document.text.strip():
        labelled = _labelled_values(document.text)
        if labelled:
            source_records = [labelled]
    if not source_records:
        raise ValueError("No structured rows or labelled key/value fields found; manual mapping is required.")

    queued: list[ReviewRecord] = []
    for source in source_records:
        record = build_review_record(
            source_name=document.source_name,
            source_sha256=document.source_sha256,
            source=source,
            workflow=workflow,
            confidence=document.confidence,
        )
        record.warnings.extend(document.warnings)
        queue.enqueue(record)
        queued.append(record)
    return queued
