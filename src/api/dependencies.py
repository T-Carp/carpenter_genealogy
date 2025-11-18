"""FastAPI dependencies for database connections and settings."""

from typing import Generator
from functools import lru_cache

from sqlalchemy.orm import Session

from ..utils.config import Settings, get_settings
from ..database.structured_store import StructuredStore
from ..visualizations.graph_builder import FamilyGraphBuilder


@lru_cache()
def get_api_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance
    """
    return get_settings()


def get_structured_store() -> Generator[StructuredStore, None, None]:
    """Get StructuredStore instance for dependency injection.

    Yields:
        StructuredStore instance
    """
    settings = get_api_settings()
    store = StructuredStore(settings)
    try:
        yield store
    finally:
        pass  # StructuredStore manages its own connections


def get_graph_builder() -> FamilyGraphBuilder:
    """Get FamilyGraphBuilder instance.

    Returns:
        FamilyGraphBuilder instance
    """
    settings = get_api_settings()
    return FamilyGraphBuilder(settings)
