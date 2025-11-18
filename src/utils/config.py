"""Configuration management for the genealogy system."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Structured Database
    structured_db_path: Path = Path("./data/structured_db/genealogy.db")

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Application Settings
    app_title: str = "Carpenter Family Genealogy"
    app_description: str = "Family genealogy data management and visualization"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
