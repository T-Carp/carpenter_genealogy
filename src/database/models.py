"""Data models for genealogy information."""

from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ConfidenceLevel(str, Enum):
    """Confidence levels for genealogical information."""

    CONFIRMED = "confirmed"
    LIKELY = "likely"
    POSSIBLE = "possible"
    UNCERTAIN = "uncertain"


class Person(BaseModel):
    """Model for a person in the genealogy."""

    id: Optional[int] = None
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    maiden_name: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    death_date: Optional[date] = None
    death_place: Optional[str] = None
    gender: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.UNCERTAIN


class Relationship(BaseModel):
    """Model for relationships between people."""

    id: Optional[int] = None
    person1_id: int
    person2_id: int
    relationship_type: str  # e.g., "parent", "spouse", "sibling"
    confidence: ConfidenceLevel = ConfidenceLevel.UNCERTAIN


class Citation(BaseModel):
    """Model for source citations."""

    id: Optional[int] = None
    source_type: str  # e.g., "book", "document", "record"
    source_name: str
    page_number: Optional[int] = None
    section: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None


class Fact(BaseModel):
    """Model for a genealogical fact."""

    id: Optional[int] = None
    person_id: int
    fact_type: str  # e.g., "birth", "death", "marriage", "immigration"
    date: Optional[date] = None
    place: Optional[str] = None
    description: str
    confidence: ConfidenceLevel = ConfidenceLevel.UNCERTAIN
    citation_id: Optional[int] = None


class QueryType(str, Enum):
    """Types of user queries."""

    FACTUAL = "factual"  # Specific fact lookup
    EXPLORATORY = "exploratory"  # Narrative/open-ended
    RELATIONSHIP = "relationship"  # About connections between people
    TIMELINE = "timeline"  # Chronological information
    LINEAGE = "lineage"  # Multi-generational lineage tracing


class QueryIntent(BaseModel):
    """Parsed user query intent."""

    original_query: str
    query_type: QueryType
    entities: list[str] = Field(default_factory=list)  # Names, places, dates mentioned
    temporal_context: Optional[str] = None  # Time period of interest
    confidence: float = 0.0


class RetrievalResult(BaseModel):
    """Result from RAG retrieval."""

    content: str
    source: str
    page_number: Optional[int] = None
    relevance_score: float
    metadata: dict = Field(default_factory=dict)


class GenealogyResponse(BaseModel):
    """Final response to user query."""

    query: str
    answer: str
    confidence: ConfidenceLevel
    citations: list[Citation] = Field(default_factory=list)
    related_people: list[str] = Field(default_factory=list)
    additional_context: Optional[str] = None
