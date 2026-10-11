import csv
import io
import json

import pytest

from packages.ingestion.phase1 import (
    IngestionError,
    dry_run_preview,
    export_reconciliation_json,
    ingest_bytes,
    normalize_header,
    validate_record,
)


def test_pasted_text_preserves_content_and_hash():
    doc = ingest_bytes("clipboard.txt", "Invoice INV-7\\nAmount 1200".encode(), pasted_text=True)
    assert doc.source_type == "pasted_text"
    assert "INV-7" in doc.text
    assert len(doc.source_sha256) == 64


def test_csv_rows_parse():
    raw = b"customer,imei,amount\\nTest User,123456789012345,1200.00\\n"
    doc = ingest_bytes("sales.csv", raw)
    assert doc.source_type == "csv"
    assert doc.rows[0]["customer"] == "Test User"
    assert doc.rows[0]["amount"] == "1200.00"


def test_unsupported_and_empty_inputs_fail_clearly():
    with pytest.raises(IngestionError, match="Unsupported file type"):
        ingest_bytes("records.exe", b"hello")
    with pytest.raises(IngestionError, match="empty"):
        ingest_bytes("empty.txt", b"")


def test_invalid_imei_is_blocked():
    result = validate_record({"imei": "12345678901234"})
    assert not result["valid"]
    assert "imei must contain exactly 15 digits." in result["errors"]


def test_missing_required_field_is_blocked():
    result = validate_record({"customer": "A"}, required_fields=("customer", "invoice_number"))
    assert not result["valid"]
    assert any("invoice_number" in issue for issue in result["errors"])


def test_negative_and_non_numeric_amounts_are_blocked():
    result = validate_record({"amount": "-10", "total": "abc"})
    assert not result["valid"]
    assert any("cannot be negative" in issue for issue in result["errors"])
    assert any("valid numeric" in issue for issue in result["errors"])


def test_dry_run_never_writes_and_json_exports():
    preview = dry_run_preview([{"customer": "Example", "amount": "100"}], target_profile="marg", module="sales")
    assert preview["mode"] == "DRY_RUN"
    assert preview["writes_performed"] is False
    assert preview["items"][0]["writes_performed"] is False
    assert json.loads(export_reconciliation_json(preview))["record_count"] == 1


def test_header_normalization():
    assert normalize_header(" GST Amount (₹) ") == "gst_amount"
