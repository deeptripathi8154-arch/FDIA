# MARG ERP and Universal Automation Agent



## Phase 3: extraction review queue and adapter safety

- `packages/review/workflow.py` maps known aliases for customer, supplier, invoice, model, IMEI, amount, payment, finance company and GST fields.
- `packages/services/review_pipeline.py` converts CSV/XLSX rows or labelled key/value text into review records. Unknown columns are retained in an unmapped-field list; arbitrary prose is not guessed into fields.
- `ReviewQueue` stores records in local SQLite, blocks duplicate source/workflow rows, requires reviewer identity, and prevents approval when deterministic validation errors remain.
- `packages/adapters/base.py` defines a narrow adapter contract and a mock adapter. MARG and generic third-party live adapter requests fail closed.
- API routes are available for pasted-text ingestion, listing review records, approving/rejecting records, dry-run preview, and mock submission. Start the API and open `/docs` to inspect them.
- Set `FDIA_REVIEW_DB` to choose the local SQLite database path. The default is `data/fdia_review_queue.sqlite3`.
- Automated tests now include review queue, pipeline and API tests. A green GitHub Actions result must still be observed before claiming the suite passes.

## Current implementation status

- Phase 1: deterministic intake for pasted text, TXT/MD/LOG, CSV, XLSX/XLSM, and text-based PDF; validation and dry-run preview only.
- Phase 2: DOCX paragraph/table extraction and image OCR through Pillow + pytesseract/Tesseract. OCR output carries an average confidence score and a warning below 80%; uncertain values require human review.
- OCR prerequisite: install the Tesseract system binary separately and make it available on PATH. Installing the Python package alone is not sufficient.
- The unified `ingest_any_bytes` entry point routes Phase 1 and Phase 2 file types. These functions do not write to MARG or any third-party app.
- Scanned PDF page rasterization, AI-assisted field mapping, durable review queue, and MARG browser/API/import integration remain future phases. Do not enable live writes until the real MARG UI and supported integration method are verified.

## Purpose
Extend FDIA into a reliable, auditable agent for turning business documents and unstructured input into validated records for MARG ERP Online and other explicitly configured business applications.

## Supported input targets
- PDF and scanned PDF
- XLSX/XLS and CSV
- DOCX and TXT
- Images and screenshots
- Raw pasted text and copied tables
- Later: authorized email/WhatsApp connector inputs

Actual format support depends on parser and test coverage. Unknown or malformed files must produce a clear error rather than silently losing data.

## Pipeline
1. Intake and classify source format.
2. Extract native text/tables; use OCR for scans and images.
3. Normalize values into a canonical, versioned record while retaining source evidence.
4. Map fields through a per-application profile.
5. Validate required fields, IMEI length, phone/GSTIN formats, dates, duplicate invoices/IMEIs, quantities, currency and tax arithmetic.
6. Display confidence, source evidence, warnings, missing fields and a proposed field-by-field change set.
7. Run dry-run by default.
8. After approval, write using a vendor-supported API/import format, or permitted browser automation when no supported integration exists.
9. Read back saved data and verify critical fields.
10. Export a reconciliation report for successful, failed, duplicate and review-required records.

## Canonical record metadata
Each record should carry source hash, source file and page/sheet/row/cell location, document type, normalized fields, field evidence and confidence, validation results, duplicate candidates, target profile/module, approval actor/time, execution state, target reference, retry count, and schema version.

## Candidate MARG retail fields
Party/customer, contact, supplier, invoice number/date, transaction type, brand, model, category, quantity, unit, rate, discount, taxable value, GST rate/amount, total, IMEI1/IMEI2/serial, payment mode, finance partner, down payment, financed amount, GSTIN/address, and source references. Confirm every required field against the actual MARG module and supported import format before live use.

## Application adapter contract
Each adapter should provide capability discovery, field validation, preview, create/update, read-back verification, and health check. Prefer official APIs and vendor-supported imports. Never invent undocumented endpoints or assume another application's field layout matches MARG.

## Reliability controls
- Never claim zero errors; use deterministic checks and a human review queue for uncertainty.
- Do not guess missing IMEIs, invoice numbers, identities, tax values, or payment amounts.
- Use idempotency keys and duplicate checks to prevent double posting.
- If a timeout occurs after a write may have succeeded, mark it SUBMISSION_UNKNOWN and reconcile before retrying.
- Retry only transient failures with bounded backoff.
- Keep source files immutable and maintain an audit trail.
- Protect credentials and customer/financial data; redact sensitive logs.
- Respect application terms and security controls; never bypass MFA, CAPTCHA or access restrictions.
- Require approval for invoices, payments, returns, stock adjustments and bulk changes until an authorized narrow policy is configured.

## Execution states
RECEIVED -> PARSED -> EXTRACTED -> VALIDATED -> NEEDS_REVIEW or READY -> APPROVED -> SUBMITTED -> VERIFIED.
Failure states: REJECTED, DUPLICATE, SUBMISSION_UNKNOWN, FAILED.

## Phased implementation
### Phase 1 — Intake and validation
Upload/paste intake, PDF/XLSX/CSV/TXT parsing, canonical schema, validation, dry-run preview, audit log, and CSV/XLSX reconciliation.

### Phase 2 — OCR and AI extraction
Scanned PDFs/images, DOCX, schema-constrained extraction, confidence scoring, and review queue.

### Phase 3 — Safe execution framework
Mock adapter, idempotency, checkpoints, bounded retries, read-back verification, and integration tests.

### Phase 4 — MARG adapter
Confirm edition/version, modules, supported API or import template, required fields, tax rules, numbering behavior, and authorized test environment. Build and test only against confirmed interfaces.

### Phase 5 — Other applications
Add one adapter and mapping profile per target application with separate permissions and tests.

### Phase 6 — Production hardening
Role-based approvals, encryption, backups, monitoring, regression tests, and deployment documentation.

## Acceptance tests
- Supported formats parse correctly; malformed/unsupported files fail clearly.
- Multi-sheet workbooks and source evidence are preserved.
- Invalid IMEI lengths and duplicate identifiers are flagged.
- Missing/low-confidence required fields block submission.
- Tax calculations use decimal arithmetic and configured rounding.
- Dry-run performs no target writes.
- A possibly successful timeout is reconciled before retry.
- Successful writes are verified by read-back.
- Every input record appears once in the reconciliation output.
- Logs do not expose passwords, tokens, or unnecessary personal data.

## Live integration prerequisites
- MARG ERP Online edition/version and exact modules.
- Official API documentation or sample supported import/export template.
- Authorized test account/company and synthetic test records.
- Required-field rules, tax configuration, numbering behavior, and user permissions.

Until these prerequisites are confirmed, the implementation should complete ingestion, extraction, validation, review, and mock-adapter tests without claiming live MARG posting works.