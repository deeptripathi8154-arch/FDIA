import pytest

from packages.ingestion.phase1 import ingest_bytes
from packages.review.workflow import ReviewQueue
from packages.services.review_pipeline import enqueue_document


def test_ingested_csv_rows_become_pending_review_records(tmp_path):
    doc = ingest_bytes(
        "sales.csv",
        b"customer,model,amount\nAsha,Phone,12000\nRavi,Tablet,20000\n",
    )
    queue = ReviewQueue(tmp_path / "queue.sqlite3")
    records = enqueue_document(doc, "sales", queue)
    assert len(records) == 2
    assert all(record.status == "pending_review" for record in records)
    assert records[0].fields["customer"] == "Asha"
    assert records[1].fields["customer"] == "Ravi"


def test_labelled_text_becomes_review_record(tmp_path):
    doc = ingest_bytes(
        "clipboard.txt",
        b"Customer: Asha\nModel: Phone\nAmount: 12000",
        pasted_text=True,
    )
    queue = ReviewQueue(tmp_path / "queue.sqlite3")
    records = enqueue_document(doc, "sales", queue)
    assert records[0].fields["customer"] == "Asha"
    assert records[0].fields["amount"] == "12000"


def test_unstructured_text_fails_closed(tmp_path):
    doc = ingest_bytes("note.txt", b"some unlabelled random text")
    with pytest.raises(ValueError, match="manual mapping"):
        enqueue_document(doc, "sales", ReviewQueue(tmp_path / "queue.sqlite3"))
