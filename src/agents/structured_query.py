"""Structured database query node for precise fact lookups."""

from typing import Any, Dict, List, Optional
from datetime import date

from ..database.structured_store import StructuredStore
from ..database.models import QueryIntent, QueryType
from ..utils.config import Settings


class StructuredQuery:
    """Queries structured database for precise genealogical facts."""

    def __init__(self, settings: Settings, structured_store: StructuredStore):
        """Initialize structured query.

        Args:
            settings: Application settings
            structured_store: Structured database instance
        """
        self.settings = settings
        self.structured_store = structured_store

    def query_person_by_name(self, first_name: str, last_name: str) -> List[Dict[str, Any]]:
        """Query for a person by name.

        Args:
            first_name: First name to search
            last_name: Last name to search

        Returns:
            List of matching persons with their information
        """
        with self.structured_store.get_session() as session:
            from ..database.structured_store import PersonDB

            results = (
                session.query(PersonDB)
                .filter(
                    PersonDB.first_name.ilike(f"%{first_name}%"),
                    PersonDB.last_name.ilike(f"%{last_name}%"),
                )
                .all()
            )

            return [
                {
                    "id": p.id,
                    "full_name": f"{p.first_name} {p.middle_name or ''} {p.last_name}".strip(),
                    "birth_date": str(p.birth_date) if p.birth_date else None,
                    "birth_place": p.birth_place,
                    "death_date": str(p.death_date) if p.death_date else None,
                    "death_place": p.death_place,
                    "confidence": p.confidence.value if p.confidence else "unknown",
                }
                for p in results
            ]

    def query_relationships(self, person_id: int) -> List[Dict[str, Any]]:
        """Query relationships for a person.

        Args:
            person_id: ID of the person

        Returns:
            List of relationships
        """
        with self.structured_store.get_session() as session:
            from ..database.structured_store import RelationshipDB, PersonDB

            relationships = (
                session.query(RelationshipDB, PersonDB)
                .filter(
                    (RelationshipDB.person1_id == person_id)
                    | (RelationshipDB.person2_id == person_id)
                )
                .join(
                    PersonDB,
                    (PersonDB.id == RelationshipDB.person2_id)
                    if RelationshipDB.person1_id == person_id
                    else (PersonDB.id == RelationshipDB.person1_id),
                )
                .all()
            )

            return [
                {
                    "related_person": f"{p.first_name} {p.last_name}",
                    "relationship_type": rel.relationship_type,
                    "confidence": rel.confidence.value if rel.confidence else "unknown",
                }
                for rel, p in relationships
            ]

    def query_facts_for_person(self, person_id: int) -> List[Dict[str, Any]]:
        """Query facts about a person.

        Args:
            person_id: ID of the person

        Returns:
            List of facts
        """
        with self.structured_store.get_session() as session:
            from ..database.structured_store import FactDB

            facts = session.query(FactDB).filter(FactDB.person_id == person_id).all()

            return [
                {
                    "type": f.fact_type,
                    "description": f.description,
                    "date": str(f.date) if f.date else None,
                    "place": f.place,
                    "confidence": f.confidence.value if f.confidence else "unknown",
                }
                for f in facts
            ]

    def build_structured_response(
        self,
        query_intent: Dict[str, Any],
    ) -> Optional[str]:
        """Build a response from structured database.

        Args:
            query_intent: Parsed query intent

        Returns:
            Response string if data found, None otherwise
        """
        entities = query_intent.get("entities", [])
        if len(entities) < 1:
            return None

        # Try to extract names from entities
        # Simple heuristic: assume first entity might be a name
        potential_names = [e for e in entities if len(e) > 2]

        if not potential_names:
            return None

        # Try querying for the first potential name
        # This is simplified - in production, use better name parsing
        name_parts = potential_names[0].split()
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = name_parts[-1]

            persons = self.query_person_by_name(first_name, last_name)

            if persons:
                response_parts = ["**Information from Structured Database:**\n"]

                for person in persons[:3]:  # Limit to 3 matches
                    response_parts.append(f"\n**{person['full_name']}**")

                    if person["birth_date"]:
                        response_parts.append(
                            f"- Born: {person['birth_date']}"
                            + (f" in {person['birth_place']}" if person["birth_place"] else "")
                        )

                    if person["death_date"]:
                        response_parts.append(
                            f"- Died: {person['death_date']}"
                            + (f" in {person['death_place']}" if person["death_place"] else "")
                        )

                    # Get relationships
                    rels = self.query_relationships(person["id"])
                    if rels:
                        response_parts.append("\n**Known Relationships:**")
                        for rel in rels:
                            response_parts.append(
                                f"- {rel['relationship_type'].title()}: {rel['related_person']}"
                            )

                    response_parts.append(
                        f"\n*Confidence: {person['confidence'].title()}*"
                    )

                return "\n".join(response_parts)

        return None

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with structured query results
        """
        query_type = state.get("query_type", "")
        query_intent = state.get("query_intent", {})

        # Only try structured query for factual queries
        if query_type != QueryType.FACTUAL.value:
            return {**state, "structured_response": None}

        structured_response = self.build_structured_response(query_intent)

        return {
            **state,
            "structured_response": structured_response,
            "has_structured_data": structured_response is not None,
        }
