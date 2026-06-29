"""Database initialization and migrations."""

from packages.database.models import Base
from packages.database.engine import get_db
from packages.logging import get_logger

logger = get_logger(__name__)


def init_db() -> None:
    """Initialize database tables."""
    db = get_db()
    db.initialize()
    
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(db.engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise


def close_db() -> None:
    """Close database connection."""
    db = get_db()
    db.close()
