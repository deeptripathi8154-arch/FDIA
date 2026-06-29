"""Database engine configuration."""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from packages.config import get_settings
from packages.logging import get_logger

logger = get_logger(__name__)


class Database:
    """Database connection manager."""

    def __init__(self) -> None:
        """Initialize database."""
        self.settings = get_settings()
        self.engine = None
        self.session_factory = None

    def initialize(self) -> None:
        """Initialize database connection."""
        db_url = self.settings.db.url
        logger.info(f"Initializing database: {db_url.replace(self.settings.db.password, '***')}")

        self.engine = create_engine(
            db_url,
            echo=self.settings.db.echo,
            pool_size=self.settings.db.pool_size,
            max_overflow=self.settings.db.max_overflow,
        )

        self.session_factory = sessionmaker(
            bind=self.engine,
            class_=Session,
            expire_on_commit=False,
        )

        logger.info("Database initialized successfully")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get database session."""
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def close(self) -> None:
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


# Global database instance
_db = Database()


def get_db() -> Database:
    """Get database instance."""
    return _db
