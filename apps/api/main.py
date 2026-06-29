"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from packages.config import get_settings
from packages.logging import get_logger

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
