import io

import pytest

from packages.ingestion.phase1 import IngestionError
from packages.ingestion.phase2 import ingest_any_bytes, ingest_phase2_bytes


def test_docx_parses_paragraphs_and_tables():
    docx = pytest.importorskip("docx")
    buffer = io.BytesIO()
    document = docx.Document()
    document.add_paragraph("Customer: Test User")
    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "IMEI"
    table.cell(0, 1).text = "123456789012345"
    document.save(buffer)

    result = ingest_phase2_bytes("invoice.docx", buffer.getvalue())
    assert result.source_type == "docx"
    assert "Customer: Test User" in result.text
    assert "123456789012345" in result.text
    assert len(result.source_sha256) == 64


def test_corrupt_docx_fails_clearly():
    pytest.importorskip("docx")
    with pytest.raises(IngestionError, match="DOCX parsing failed"):
        ingest_phase2_bytes("invoice.docx", b"not a real docx")


def test_image_requires_real_ocr_runtime_or_extracts_text(monkeypatch):
    Image = pytest.importorskip("PIL.Image")
    pytest.importorskip("pytesseract")
    buffer = io.BytesIO()
    Image.new("RGB", (40, 20), "white").save(buffer, format="PNG")

    class FakeOutput:
        DICT = "dict"

    class FakeTesseract:
        Output = FakeOutput
        TesseractNotFoundError = Exception

        @staticmethod
        def image_to_data(image, output_type, config):
            return {"text": ["Invoice", "123"], "conf": ["95", "80"]}

    monkeypatch.setitem(__import__("sys").modules, "pytesseract", FakeTesseract)
    result = ingest_phase2_bytes("scan.png", buffer.getvalue())
    assert result.source_type == "image_ocr"
    assert result.text == "Invoice 123"
    assert abs(result.confidence - 0.875) < 0.0001


def test_unified_ingestion_routes_phase1_formats():
    result = ingest_any_bytes("note.txt", b"hello")
    assert result.source_type == "text"


def test_unsupported_phase2_extension_fails():
    with pytest.raises(IngestionError, match="Phase 2 supports DOCX"):
        ingest_phase2_bytes("archive.zip", b"abc")
