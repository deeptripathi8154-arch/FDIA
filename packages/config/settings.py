"""Application settings using pydantic-settings."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration."""

    driver: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    user: str = "fdia_user"
    password: str = "changeme"
    name: str = "fdia_db"
    echo: bool = False
    pool_size: int = 20
    max_overflow: int = 40

    @property
    def url(self) -> str:
        """Get database URL."""
        return (
            f"{self.driver}://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class OcrSettings(BaseSettings):
    """OCR configuration."""

    engine: str = "paddleocr"
    languages: list[str] = ["en", "es"]
    confidence_threshold: float = 0.5


class AiSettings(BaseSettings):
    """AI/LLM configuration."""

    model_url: str = "http://localhost:11434"
    model_name: str = "llama2"
    temperature: float = 0.7
    max_tokens: int = 2048


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    # App
    app_env: str = "development"
    app_debug: bool = False
    app_version: str = "0.1.0"

    # Database
    db: DatabaseSettings = DatabaseSettings()

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # OCR
    ocr: OcrSettings = OcrSettings()

    # AI
    ai: AiSettings = AiSettings()

    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Storage
    storage_base_path: str = "./data"
    max_file_size_mb: int = 100

    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/fdia.log"

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.app_env == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
