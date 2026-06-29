"""Base repository interface."""

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar
from uuid import UUID

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Base repository interface."""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create entity."""
        pass

    @abstractmethod
    def read(self, entity_id: UUID) -> Optional[T]:
        """Read entity."""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update entity."""
        pass

    @abstractmethod
    def delete(self, entity_id: UUID) -> bool:
        """Delete entity."""
        pass

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        """List entities."""
        pass
