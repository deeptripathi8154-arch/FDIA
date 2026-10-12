"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from dataclasses import asdict
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from packages.config import get_settings
from packages.logging import get_logger
from packages.adapters.base import MockAdapter
from packages.ingestion.phase1 import IngestionError, ingest_bytes
from packages.review.workflow import ReviewQueue
from packages.services.review_pipeline import enqueue_document

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting FDIA API...")
    yield
    logger.info("Shutting down FDIA API...")


def create_app() -> FastAPI:
    """Create FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Finance Document Intelligence Agent",
        description="Enterprise Finance Document Processing Platform",
        version=settings.app_version,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.app_debug else ["http://localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check
    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        """Health check endpoint."""
        return {"status": "ok", "version": settings.app_version}


    def review_queue() -> ReviewQueue:
        return ReviewQueue(os.getenv("FDIA_REVIEW_DB", "data/fdia_review_queue.sqlite3"))

    @app.post("/api/v1/review/ingest-text", tags=["Review"])
    async def ingest_text_for_review(payload: dict) -> dict:
        """Ingest pasted text into the human-review queue; never writes to an ERP."""
        filename = str(payload.get("filename", "clipboard.txt"))
        content = payload.get("text")
        workflow = str(payload.get("workflow", "sales"))
        if not isinstance(content, str) or not content.strip():
            raise HTTPException(status_code=422, detail="A non-empty text field is required.")
        try:
            document = ingest_bytes(filename, content.encode("utf-8"), pasted_text=True)
            records = enqueue_document(document, workflow, review_queue())
        except (ValueError, IngestionError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {"source_sha256": document.source_sha256, "queued": len(records),
                "records": [asdict(record) for record in records]}

    @app.get("/api/v1/review/records", tags=["Review"])
    async def list_review_records(status: str = "pending_review") -> dict:
        try:
            records = review_queue().list_records(status=status)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {"records": [asdict(record) for record in records], "total": len(records)}

    @app.post("/api/v1/review/records/{record_id}/decision", tags=["Review"])
    async def decide_review_record(record_id: str, payload: dict) -> dict:
        reviewer = str(payload.get("reviewer", "")).strip()
        decision = payload.get("decision")
        if decision not in {"approve", "reject"}:
            raise HTTPException(status_code=422, detail="decision must be 'approve' or 'reject'.")
        try:
            record = review_queue().review(record_id, reviewer, approve=(decision == "approve"))
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Review record not found.") from exc
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return asdict(record)

    @app.post("/api/v1/review/records/{record_id}/preview", tags=["Adapters"])
    async def preview_record(record_id: str) -> dict:
        """Build a mock adapter preview only; no external application is modified."""
        try:
            record = review_queue().get(record_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Review record not found.") from exc
        return asdict(MockAdapter().preview(record))

    @app.post("/api/v1/review/records/{record_id}/mock-submit", tags=["Adapters"])
    async def mock_submit_record(record_id: str) -> dict:
        """Simulate a submission after approval; this is not a live ERP write."""
        try:
            record = review_queue().get(record_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Review record not found.") from exc
        return asdict(MockAdapter().submit(record))

    # API Routes (TODO: Add more endpoints)
    @app.get("/api/v1/documents", tags=["Documents"])
    async def list_documents() -> dict:
        """List all documents."""
        return {"documents": [], "total": 0}

    @app.get("/api/v1/documents/{document_id}", tags=["Documents"])
    async def get_document(document_id: str) -> dict:
        """Get specific document."""
        return {"document_id": document_id, "status": "not_found"}

    logger.info("FastAPI application created successfully")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_debug,
    )
