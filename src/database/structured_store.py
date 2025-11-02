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
    """Person table - renamed from people to persons for consistency."""

    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    given_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    surname = Column(String, nullable=False)
    maiden_name = Column(String, nullable=True)
    birth_year = Column(Integer, nullable=True)
    death_year = Column(Integer, nullable=True)
    generation = Column(Integer, nullable=True)
    confidence = Column(SQLEnum(ConfidenceLevel), default=ConfidenceLevel.UNCERTAIN)


class RelationshipDB(Base):
    """Parent-child relationship table."""

    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    child_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    relationship_type = Column(String, nullable=False)  # biological, adoptive, step
    confidence = Column(SQLEnum(ConfidenceLevel), default=ConfidenceLevel.UNCERTAIN)


class PartnershipDB(Base):
    """Partnership/Marriage table."""

    __tablename__ = "partnerships"

    id = Column(Integer, primary_key=True)
    person1_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    person2_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    partnership_type = Column(String, nullable=False)  # marriage, partnership
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    sequence_number = Column(Integer, nullable=True)
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


class FactDB(Base):
    """Fact table."""

    __tablename__ = "facts"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    fact_type = Column(String, nullable=False)
    date = Column(Date, nullable=True)
    place = Column(String, nullable=True)
    description = Column(String, nullable=False)
    confidence = Column(SQLEnum(ConfidenceLevel), default=ConfidenceLevel.UNCERTAIN)
    citation_id = Column(Integer, ForeignKey("citations.id"), nullable=True)


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

    def add_person(self, person_or_given_name, surname=None, **kwargs) -> int:
        """Add a person to the database.

        Can accept either a Person model object or individual parameters.

        Args:
            person_or_given_name: Person model object OR given_name string
            surname: Surname (if using individual params)
            **kwargs: Additional person fields (generation, birth_year, etc.)

        Returns:
            ID of the created person
        """
        with self.get_session() as session:
            # Check if first arg is a Pydantic model
            if hasattr(person_or_given_name, 'model_dump'):
                person_dict = person_or_given_name.model_dump()
                person_db = PersonDB(**{k: v for k, v in person_dict.items() if k != 'id'})
            else:
                # Individual parameters
                person_db = PersonDB(
                    given_name=person_or_given_name,
                    surname=surname,
                    middle_name=kwargs.get('middle_name'),
                    maiden_name=kwargs.get('maiden_name'),
                    birth_year=kwargs.get('birth_year'),
                    death_year=kwargs.get('death_year'),
                    generation=kwargs.get('generation'),
                    confidence=kwargs.get('confidence', ConfidenceLevel.UNCERTAIN),
                )

            session.add(person_db)
            session.commit()
            session.refresh(person_db)
            return person_db.id

    def search_person(self, given_name: str, surname: str) -> List[PersonDB]:
        """Search for a person by name.

        Args:
            given_name: Given name to search
            surname: Surname to search

        Returns:
            List of matching persons
        """
        with self.get_session() as session:
            return (
                session.query(PersonDB)
                .filter(
                    PersonDB.given_name.ilike(f"%{given_name}%"),
                    PersonDB.surname.ilike(f"%{surname}%"),
                )
                .all()
            )

    def add_relationship(self, rel_or_parent_id, child_id=None, relationship_type=None, confidence=None) -> int:
        """Add a parent-child relationship.

        Can accept either a Relationship model object or individual parameters.

        Args:
            rel_or_parent_id: Relationship model OR parent_id int
            child_id: Child person ID (if using individual params)
            relationship_type: Type of relationship (if using individual params)
            confidence: Confidence level (if using individual params)

        Returns:
            ID of the created relationship
        """
        with self.get_session() as session:
            # Check if first arg is a Pydantic model
            if hasattr(rel_or_parent_id, 'model_dump'):
                rel_dict = rel_or_parent_id.model_dump()
                rel_db = RelationshipDB(**{k: v for k, v in rel_dict.items() if k != 'id'})
            else:
                # Individual parameters
                rel_db = RelationshipDB(
                    parent_id=rel_or_parent_id,
                    child_id=child_id,
                    relationship_type=relationship_type,
                    confidence=confidence if confidence else ConfidenceLevel.UNCERTAIN,
                )

            session.add(rel_db)
            session.commit()
            session.refresh(rel_db)
            return rel_db.id

    def add_partnership(self, partnership_or_person1_id, person2_id=None, partnership_type="marriage", **kwargs) -> int:
        """Add a partnership/marriage.

        Args:
            partnership_or_person1_id: Partnership model OR person1_id int
            person2_id: Second person ID (if using individual params)
            partnership_type: Type of partnership (default: marriage)
            **kwargs: Additional partnership fields

        Returns:
            ID of the created partnership
        """
        with self.get_session() as session:
            # Check if first arg is a Pydantic model
            if hasattr(partnership_or_person1_id, 'model_dump'):
                part_dict = partnership_or_person1_id.model_dump()
                part_db = PartnershipDB(**{k: v for k, v in part_dict.items() if k != 'id'})
            else:
                # Individual parameters
                part_db = PartnershipDB(
                    person1_id=partnership_or_person1_id,
                    person2_id=person2_id,
                    partnership_type=partnership_type,
                    start_year=kwargs.get('start_year'),
                    end_year=kwargs.get('end_year'),
                    sequence_number=kwargs.get('sequence_number'),
                    confidence=kwargs.get('confidence', ConfidenceLevel.UNCERTAIN),
                )

            session.add(part_db)
            session.commit()
            session.refresh(part_db)
            return part_db.id

    def get_relationships(self, person_id: int) -> List[RelationshipDB]:
        """Get all parent-child relationships for a person.

        Args:
            person_id: ID of the person

        Returns:
            List of relationships where person is parent or child
        """
        with self.get_session() as session:
            return (
                session.query(RelationshipDB)
                .filter(
                    (RelationshipDB.parent_id == person_id)
                    | (RelationshipDB.child_id == person_id)
                )
                .all()
            )

    def get_partnerships(self, person_id: int) -> List[PartnershipDB]:
        """Get all partnerships for a person.

        Args:
            person_id: ID of the person

        Returns:
            List of partnerships
        """
        with self.get_session() as session:
            return (
                session.query(PartnershipDB)
                .filter(
                    (PartnershipDB.person1_id == person_id)
                    | (PartnershipDB.person2_id == person_id)
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

    def find_person_by_name(self, given_name: str, surname: str):
        """Find a person by exact given name and surname match.

        Args:
            given_name: Given name
            surname: Surname

        Returns:
            Person Pydantic model if found, None otherwise
        """
        from ..database.models import Person

        with self.get_session() as session:
            person_db = (
                session.query(PersonDB)
                .filter(
                    PersonDB.given_name == given_name,
                    PersonDB.surname == surname,
                )
                .first()
            )

            if not person_db:
                return None

            # Convert to Pydantic model
            return Person(
                id=person_db.id,
                given_name=person_db.given_name,
                middle_name=person_db.middle_name,
                surname=person_db.surname,
                maiden_name=person_db.maiden_name,
                birth_year=person_db.birth_year,
                death_year=person_db.death_year,
                generation=person_db.generation,
                confidence=person_db.confidence,
            )

    def get_person_by_id(self, person_id: int):
        """Get a person by ID.

        Args:
            person_id: Person ID

        Returns:
            Person Pydantic model if found, None otherwise
        """
        from ..database.models import Person

        with self.get_session() as session:
            person_db = session.query(PersonDB).filter(PersonDB.id == person_id).first()

            if not person_db:
                return None

            return Person(
                id=person_db.id,
                given_name=person_db.given_name,
                middle_name=person_db.middle_name,
                surname=person_db.surname,
                maiden_name=person_db.maiden_name,
                birth_year=person_db.birth_year,
                death_year=person_db.death_year,
                generation=person_db.generation,
                confidence=person_db.confidence,
            )

    def has_relationship(self, parent_id: int, child_id: int, rel_type: str) -> bool:
        """Check if a parent-child relationship already exists.

        Args:
            parent_id: Parent person ID
            child_id: Child person ID
            rel_type: Relationship type

        Returns:
            True if relationship exists
        """
        with self.get_session() as session:
            exists = (
                session.query(RelationshipDB)
                .filter(
                    RelationshipDB.parent_id == parent_id,
                    RelationshipDB.child_id == child_id,
                    RelationshipDB.relationship_type == rel_type,
                )
                .first()
            )
            return exists is not None

    def has_partnership(self, person1_id: int, person2_id: int) -> bool:
        """Check if a partnership already exists between two people.

        Args:
            person1_id: First person ID
            person2_id: Second person ID

        Returns:
            True if partnership exists
        """
        with self.get_session() as session:
            exists = (
                session.query(PartnershipDB)
                .filter(
                    ((PartnershipDB.person1_id == person1_id) & (PartnershipDB.person2_id == person2_id))
                    | ((PartnershipDB.person1_id == person2_id) & (PartnershipDB.person2_id == person1_id))
                )
                .first()
            )
            return exists is not None

    def get_all_people(self) -> List[PersonDB]:
        """Get all people from the database.

        Returns:
            List of all PersonDB objects
        """
        with self.get_session() as session:
            return session.query(PersonDB).all()

    def clear_all_data(self):
        """Clear all data from the database. Use with caution!"""
        with self.get_session() as session:
            session.query(FactDB).delete()
            session.query(PartnershipDB).delete()
            session.query(RelationshipDB).delete()
            session.query(PersonDB).delete()
            session.query(CitationDB).delete()
            session.commit()
            print("All structured data cleared from database")
