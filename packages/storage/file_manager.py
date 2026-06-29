"""File storage management."""

from pathlib import Path
from typing import Optional

from packages.config import get_settings
from packages.logging import get_logger

logger = get_logger(__name__)


class FileManager:
    """File storage management."""

    def __init__(self) -> None:
        """Initialize file manager."""
        self.settings = get_settings()
        self.base_path = Path(self.settings.storage_base_path)
        self._create_directories()

    def _create_directories(self) -> None:
        """Create necessary storage directories."""
        directories = [
            "downloads",
            "processed",
            "failed",
            "images",
            "pdfs",
            "excel",
            "database",
            "backups",
        ]
        
        for directory in directories:
            path = self.base_path / directory
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Storage directory ready: {path}")

    def get_downloads_path(self) -> Path:
        """Get downloads directory path."""
        return self.base_path / "downloads"

    def get_processed_path(self) -> Path:
        """Get processed directory path."""
        return self.base_path / "processed"

    def get_failed_path(self) -> Path:
        """Get failed directory path."""
        return self.base_path / "failed"

    def get_images_path(self) -> Path:
        """Get images directory path."""
        return self.base_path / "images"

    def get_pdfs_path(self) -> Path:
        """Get PDFs directory path."""
        return self.base_path / "pdfs"

    def get_excel_path(self) -> Path:
        """Get Excel directory path."""
        return self.base_path / "excel"

    def save_file(self, source_path: Path, destination_dir: str) -> Optional[Path]:
        """Save file to storage.
        
        Args:
            source_path: Source file path
            destination_dir: Destination directory name
            
        Returns:
            Saved file path or None
        """
        try:
            dest_path = self.base_path / destination_dir / source_path.name
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            # TODO: Implement file copy/move
            logger.info(f"File saved: {dest_path}")
            return dest_path
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            return None

    def delete_file(self, file_path: Path) -> bool:
        """Delete file.
        
        Args:
            file_path: File path to delete
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False
