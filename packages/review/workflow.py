"""Deterministic extraction mapping, validation and human approval queue.

This module deliberately has no ERP write capability. Review records are persisted
locally in SQLite and can only be approved by an explicit reviewer action.
"""
from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from packages.ingestion.phase1 import validate_record

FIELD_ALIASES = {
    "customer": {"customer", "customer_name", "party", "party_name", "name", "client"},
    "customer_phone": {"customer_phone", "phone", "mobile", "mobile_number", "contact"},
    "invoice_number": {"invoice", "invoice_no", "invoice_number", "bill_no", "bill_number", "voucher_no"},
    "date": {"date", "invoice_date", "bill_date", "voucher_date"},
    "brand": {"brand", "make", "manufacturer"},
    "model": {"model", "device_model", "product", "product_name", "item", "item_name"},
    "imei": {"imei", "imei1", "imei_1", "imei_number"},
    "imei2": {"imei2", "imei_2", "second_imei"},
    "serial_number": {"serial", "serial_no", "serial_number", "sn"},
    "quantity": {"qty", "quantity", "units"},
    "amount": {"amount", "price", "product_amount", "sale_amount", "purchase_amount", "mrp"},
    "down_payment": {"downpayment", "down_payment", "dp", "customer_contribution"},
    "finance_company": {"finance_company", "financier", "finance", "lender"},
    "payment_mode": {"payment_mode", "payment", "mode_of_payment"},
    "gst_number": {"gst", "gstin", "gst_number", "gst_no"},
    "supplier": {"supplier", "vendor", "supplier_name", "vendor_name"},
}

DEFAULT_REQUIRED_BY_WORKFLOW = {
    "purchase": ("supplier", "model", "amount"),
    "sales": ("customer", "model", "amount"),
    "inventory": ("model",),
    "finance": ("customer", "finance_company", "amount"),
    "customer": ("customer",),
}


def _key(value: str) -> str:
    return "".join(ch for ch in str(value).strip().lower() if ch.isalnum())


_ALIAS_INDEX = {_key(alias): canonical for canonical, aliases in FIELD_ALIASES.items() for alias in aliases}


def map_fields(source: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    """Map known header/label aliases; preserve unmapped values for review."""
    mapped: dict[str, str] = {}
    unmapped: list[str] = []
    for raw_key, raw_value in source.items():
        canonical = _ALIAS_INDEX.get(_key(raw_key))
        if not canonical:
            unmapped.append(str(raw_key))
            continue
        value = "" if raw_value is None else str(raw_value).strip()
        if canonical in mapped and mapped[canonical] and value and mapped[canonical] != value:
            unmapped.append(str(raw_key))
            continue
        mapped[canonical] = value
    return mapped, unmapped


@dataclass
class ReviewRecord:
    id: str
    source_name: str
    source_sha256: str
    workflow: str
    fields: dict[str, str]
    unmapped_fields: list[str]
    errors: list[str]
    warnings: list[str]
    confidence: float | None
    status: str = "pending_review"
    reviewer: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reviewed_at: str | None = None
    adapter_result: dict[str, Any] | None = None


def build_review_record(source_name: str, source_sha256: str, source: dict[str, Any],
                        workflow: str, *, confidence: float | None = None,
                        required_fields: Iterable[str] | None = None) -> ReviewRecord:
    workflow = workflow.strip().lower()
    if workflow not in DEFAULT_REQUIRED_BY_WORKFLOW:
        raise ValueError(f"Unsupported workflow: {workflow}")
    fields, unmapped = map_fields(source)
    required = tuple(required_fields) if required_fields is not None else DEFAULT_REQUIRED_BY_WORKFLOW[workflow]
    validation = validate_record(fields, required_fields=required)
    warnings = []
    if confidence is not None and confidence < 0.80:
        warnings.append("Extraction confidence is below 80%; verify every field.")
    if unmapped:
        warnings.append("Unmapped source fields require manual mapping.")
    return ReviewRecord(
        id=str(uuid.uuid4()), source_name=source_name, source_sha256=source_sha256,
        workflow=workflow, fields=fields, unmapped_fields=unmapped,
        errors=validation["errors"], warnings=warnings, confidence=confidence,
    )


class ReviewQueue:
    """Small local SQLite review queue with duplicate-source protection."""

    def __init__(self, db_path: str | Path = "data/fdia_review_queue.sqlite3") -> None:
        self.db_path = str(db_path)
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS review_records (
                id TEXT PRIMARY KEY, source_sha256 TEXT NOT NULL, workflow TEXT NOT NULL,
                status TEXT NOT NULL, payload TEXT NOT NULL, reviewer TEXT,
                created_at TEXT NOT NULL, reviewed_at TEXT,
                UNIQUE(source_sha256, workflow)
            )""")

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def enqueue(self, record: ReviewRecord) -> ReviewRecord:
        payload = json.dumps(asdict(record), ensure_ascii=False)
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO review_records VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (record.id, record.source_sha256, record.workflow, record.status,
                     payload, record.reviewer, record.created_at, record.reviewed_at),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError("This source hash is already queued for this workflow.") from exc
        return record

    def list_records(self, status: str | None = "pending_review") -> list[ReviewRecord]:
        query = "SELECT payload FROM review_records"
        params: tuple[Any, ...] = ()
        if status is not None:
            query += " WHERE status = ?"
            params = (status,)
        query += " ORDER BY created_at"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [ReviewRecord(**json.loads(row["payload"])) for row in rows]

    def get(self, record_id: str) -> ReviewRecord:
        with self._connect() as conn:
            row = conn.execute("SELECT payload FROM review_records WHERE id = ?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return ReviewRecord(**json.loads(row["payload"]))

    def review(self, record_id: str, reviewer: str, *, approve: bool) -> ReviewRecord:
        reviewer = reviewer.strip()
        if not reviewer:
            raise ValueError("A reviewer identity is required.")
        record = self.get(record_id)
        if record.status != "pending_review":
            raise ValueError(f"Record cannot be reviewed from status {record.status}.")
        if approve and record.errors:
            raise ValueError("Record has validation errors and cannot be approved.")
        record.status = "approved" if approve else "rejected"
        record.reviewer = reviewer
        record.reviewed_at = datetime.now(timezone.utc).isoformat()
        payload = json.dumps(asdict(record), ensure_ascii=False)
        with self._connect() as conn:
            conn.execute(
                "UPDATE review_records SET status=?, payload=?, reviewer=?, reviewed_at=? WHERE id=?",
                (record.status, payload, reviewer, record.reviewed_at, record.id),
            )
        return record
