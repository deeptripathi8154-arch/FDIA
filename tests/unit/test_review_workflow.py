import pytest

from packages.adapters.base import LiveWritesDisabled, MockAdapter, get_adapter
from packages.review.workflow import ReviewQueue, build_review_record, map_fields


def test_alias_mapping_preserves_unmapped_fields():
    mapped, unmapped = map_fields({
        "Customer Name": "Asha",
        "IMEI1": "123456789012345",
        "Odd Column": "keep me",
    })
    assert mapped["customer"] == "Asha"
    assert mapped["imei"] == "123456789012345"
    assert unmapped == ["Odd Column"]


def test_queue_requires_review_and_blocks_duplicate_source(tmp_path):
    queue = ReviewQueue(tmp_path / "review.sqlite3")
    record = build_review_record(
        "sale.csv", "a" * 64,
        {"customer": "Asha", "model": "Phone", "amount": "12000"},
        "sales",
    )
    queue.enqueue(record)
    assert queue.get(record.id).status == "pending_review"
    with pytest.raises(ValueError, match="already queued"):
        queue.enqueue(record)
    approved = queue.review(record.id, "operator-1", approve=True)
    assert approved.status == "approved"
    assert approved.reviewer == "operator-1"
    assert approved.reviewed_at


def test_invalid_record_cannot_be_approved(tmp_path):
    queue = ReviewQueue(tmp_path / "review.sqlite3")
    record = build_review_record("sale.csv", "b" * 64, {"customer": "Asha"}, "sales")
    queue.enqueue(record)
    assert record.errors
    with pytest.raises(ValueError, match="validation errors"):
        queue.review(record.id, "operator-1", approve=True)


def test_low_confidence_and_unmapped_fields_warn(tmp_path):
    record = build_review_record(
        "scan.png", "c" * 64,
        {"customer": "Asha", "model": "Phone", "amount": "5000", "random": "x"},
        "sales", confidence=0.42,
    )
    assert len(record.warnings) == 2
    assert record.unmapped_fields == ["random"]


def test_mock_adapter_never_claims_live_verification(tmp_path):
    record = build_review_record(
        "sale.csv", "d" * 64,
        {"customer": "Asha", "model": "Phone", "amount": "5000"},
        "sales",
    )
    adapter = MockAdapter()
    assert adapter.preview(record).mode == "dry_run"
    assert not adapter.preview(record).verified
    assert not adapter.submit(record).success
    record.status = "approved"
    result = adapter.submit(record)
    assert result.success and result.mode == "mock" and not result.verified
    with pytest.raises(LiveWritesDisabled):
        get_adapter("marg", allow_live=True)
