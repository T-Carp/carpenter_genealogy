"""Tests for database operations."""

import pytest
from datetime import date
from pathlib import Path
import tempfile
from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import Settings


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        settings = Settings(
            anthropic_api_key="test-key",
            structured_db_path=Path(tmpdir) / "test.db",
        )
        store = StructuredStore(settings)
        yield store


def test_add_person(temp_db):
    """Test adding a person to the database."""
    person_id = temp_db.add_person(
        first_name="John",
        last_name="Carpenter",
        birth_date=date(1850, 1, 1),
        birth_place="Pennsylvania",
        confidence=ConfidenceLevel.CONFIRMED,
    )

    assert person_id is not None
    assert isinstance(person_id, int)


def test_search_person(temp_db):
    """Test searching for a person."""
    # Add test person
    temp_db.add_person(
        first_name="Mary",
        last_name="Smith",
        birth_date=date(1860, 5, 15),
    )

    # Search
    results = temp_db.search_person("Mary", "Smith")

    assert len(results) > 0
    assert results[0].first_name == "Mary"
    assert results[0].last_name == "Smith"


def test_add_relationship(temp_db):
    """Test adding a relationship."""
    # Add two people
    person1_id = temp_db.add_person("John", "Carpenter")
    person2_id = temp_db.add_person("Mary", "Carpenter")

    # Add relationship
    rel_id = temp_db.add_relationship(
        person1_id,
        person2_id,
        "spouse",
        ConfidenceLevel.CONFIRMED,
    )

    assert rel_id is not None

    # Get relationships
    rels = temp_db.get_relationships(person1_id)
    assert len(rels) > 0
    assert rels[0].relationship_type == "spouse"


def test_add_fact(temp_db):
    """Test adding a fact about a person."""
    # Add person
    person_id = temp_db.add_person("Thomas", "Carpenter")

    # Add fact
    fact_id = temp_db.add_fact(
        person_id=person_id,
        fact_type="birth",
        description="Born in Philadelphia",
        date=date(1820, 3, 10),
        place="Philadelphia, PA",
        confidence=ConfidenceLevel.LIKELY,
    )

    assert fact_id is not None
