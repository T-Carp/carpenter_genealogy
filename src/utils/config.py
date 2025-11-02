"""Configuration management for the genealogy system."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Anthropic API
    anthropic_api_key: str
    claude_model: str = "claude-3-5-sonnet-20241022"

    # Vector Database
    vector_db_path: Path = Path("./data/vector_store")
    vector_db_collection: str = "genealogy_narratives"

    # Structured Database
    structured_db_path: Path = Path("./data/structured_db/genealogy.db")

    # Neo4j (optional)
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    # Application Settings
    max_context_chunks: int = 10
    chunk_size: int = 1000
    chunk_overlap: int = 200
    confidence_threshold: float = 0.7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
