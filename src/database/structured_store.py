"""Structured database for genealogical facts and relationships."""

from datetime import date
from pathlib import Path
from typing import List, Optional
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Float,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

from .models import ConfidenceLevel
from ..utils.config import Settings

Base = declarative_base()


class PersonDB(Base):
    """Person table."""

    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    maiden_name = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    birth_place = Column(String, nullable=True)
    death_date = Column(Date, nullable=True)
    death_place = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    confidence = Column(SQLEnum(ConfidenceLevel), default=ConfidenceLevel.UNCERTAIN)

    # Relationships
    facts = relationship("FactDB", back_populates="person")


class RelationshipDB(Base):
    """Relationship table."""

    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)
    person1_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person2_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    relationship_type = Column(String, nullable=False)
    confidence = Column(SQLEnum(ConfidenceLevel), default=ConfidenceLevel.UNCERTAIN)


class CitationDB(Base):
    """Citation table."""

    __tablename__ = "citations"

    id = Column(Integer, primary_key=True)
    source_type = Column(String, nullable=False)
    source_name = Column(String, nullable=False)
    page_number = Column(Integer, nullable=True)
    section = Column(String, nullable=True)
    url = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    # Relationships
    facts = relationship("FactDB", back_populates="citation")


class FactDB(Base):
    """Fact table."""

    __tablename__ = "facts"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    fact_type = Column(String, nullable=False)
    date = Column(Date, nullable=True)
    place = Column(String, nullable=True)
    description = Column(String, nullable=False)
    confidence = Column(SQLEnum(ConfidenceLevel), default=ConfidenceLevel.UNCERTAIN)
    citation_id = Column(Integer, ForeignKey("citations.id"), nullable=True)

    # Relationships
    person = relationship("PersonDB", back_populates="facts")
    citation = relationship("CitationDB", back_populates="facts")


class StructuredStore:
    """Interface for structured genealogy database."""

    def __init__(self, settings: Settings):
        """Initialize structured database.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.settings.structured_db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create engine and session
        db_url = f"sqlite:///{self.settings.structured_db_path}"
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)

        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()

    def add_person(
        self,
        first_name: str,
        last_name: str,
        middle_name: Optional[str] = None,
        maiden_name: Optional[str] = None,
        birth_date: Optional[date] = None,
        birth_place: Optional[str] = None,
        death_date: Optional[date] = None,
        death_place: Optional[str] = None,
        gender: Optional[str] = None,
        confidence: ConfidenceLevel = ConfidenceLevel.UNCERTAIN,
    ) -> int:
        """Add a person to the database.

        Returns:
            ID of the created person
        """
        with self.get_session() as session:
            person = PersonDB(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                maiden_name=maiden_name,
                birth_date=birth_date,
                birth_place=birth_place,
                death_date=death_date,
                death_place=death_place,
                gender=gender,
                confidence=confidence,
            )
            session.add(person)
            session.commit()
            session.refresh(person)
            return person.id

    def search_person(self, first_name: str, last_name: str) -> List[PersonDB]:
        """Search for a person by name.

        Args:
            first_name: First name to search
            last_name: Last name to search

        Returns:
            List of matching persons
        """
        with self.get_session() as session:
            return (
                session.query(PersonDB)
                .filter(
                    PersonDB.first_name.ilike(f"%{first_name}%"),
                    PersonDB.last_name.ilike(f"%{last_name}%"),
                )
                .all()
            )

    def add_relationship(
        self,
        person1_id: int,
        person2_id: int,
        relationship_type: str,
        confidence: ConfidenceLevel = ConfidenceLevel.UNCERTAIN,
    ) -> int:
        """Add a relationship between two people.

        Returns:
            ID of the created relationship
        """
        with self.get_session() as session:
            rel = RelationshipDB(
                person1_id=person1_id,
                person2_id=person2_id,
                relationship_type=relationship_type,
                confidence=confidence,
            )
            session.add(rel)
            session.commit()
            session.refresh(rel)
            return rel.id

    def get_relationships(self, person_id: int) -> List[RelationshipDB]:
        """Get all relationships for a person.

        Args:
            person_id: ID of the person

        Returns:
            List of relationships
        """
        with self.get_session() as session:
            return (
                session.query(RelationshipDB)
                .filter(
                    (RelationshipDB.person1_id == person_id)
                    | (RelationshipDB.person2_id == person_id)
                )
                .all()
            )

    def add_fact(
        self,
        person_id: int,
        fact_type: str,
        description: str,
        date: Optional[date] = None,
        place: Optional[str] = None,
        confidence: ConfidenceLevel = ConfidenceLevel.UNCERTAIN,
        citation_id: Optional[int] = None,
    ) -> int:
        """Add a fact about a person.

        Returns:
            ID of the created fact
        """
        with self.get_session() as session:
            fact = FactDB(
                person_id=person_id,
                fact_type=fact_type,
                description=description,
                date=date,
                place=place,
                confidence=confidence,
                citation_id=citation_id,
            )
            session.add(fact)
            session.commit()
            session.refresh(fact)
            return fact.id
