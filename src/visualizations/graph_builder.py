"""Graph builder for family tree visualization."""

from typing import List, Optional, Set, Dict, Tuple
import networkx as nx
from sqlalchemy.orm import Session

from ..database.structured_store import StructuredStore, PersonDB, RelationshipDB, PartnershipDB
from ..utils.config import Settings


class FamilyGraphBuilder:
    """Builds NetworkX graph from genealogy database."""

    def __init__(self, settings: Settings):
        """Initialize graph builder.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.store = StructuredStore(settings)

    def build_graph(
        self,
        root_person_id: Optional[int] = None,
        max_generations: Optional[int] = None,
        include_ancestors: bool = True,
        include_descendants: bool = True,
        surname_filter: Optional[str] = None,
    ) -> nx.DiGraph:
        """Build a directed graph of family relationships.

        Args:
            root_person_id: Starting person ID (if None, includes all people)
            max_generations: Maximum generations from root (if None, unlimited)
            include_ancestors: Include ancestors of root person
            include_descendants: Include descendants of root person
            surname_filter: Only include people with this surname

        Returns:
            NetworkX directed graph with person nodes and relationship edges
        """
        G = nx.DiGraph()

        with self.store.get_session() as session:
            # Determine which people to include
            if root_person_id:
                person_ids = self._get_related_people(
                    session,
                    root_person_id,
                    max_generations,
                    include_ancestors,
                    include_descendants,
                )
            else:
                # Get all people
                people = session.query(PersonDB).all()
                person_ids = {p.id for p in people}

            # Apply surname filter if specified
            if surname_filter:
                people = session.query(PersonDB).filter(
                    PersonDB.id.in_(person_ids),
                    PersonDB.surname == surname_filter
                ).all()
                person_ids = {p.id for p in people}

            # Add nodes for each person
            for person_id in person_ids:
                person = session.query(PersonDB).get(person_id)
                if person:
                    self._add_person_node(G, person)

            # Add edges for parent-child relationships
            relationships = session.query(RelationshipDB).filter(
                RelationshipDB.parent_id.in_(person_ids),
                RelationshipDB.child_id.in_(person_ids),
            ).all()

            for rel in relationships:
                G.add_edge(
                    rel.parent_id,
                    rel.child_id,
                    edge_type="parent_child",
                    relationship_type=rel.relationship_type,
                    confidence=rel.confidence.value if rel.confidence else "uncertain",
                )

            # Add partnership information as node attributes
            partnerships = session.query(PartnershipDB).filter(
                PartnershipDB.person1_id.in_(person_ids),
                PartnershipDB.person2_id.in_(person_ids),
            ).all()

            # Store partnerships for each person
            for part in partnerships:
                # Add partnership data to both nodes
                if part.person1_id in G.nodes:
                    if "partnerships" not in G.nodes[part.person1_id]:
                        G.nodes[part.person1_id]["partnerships"] = []
                    G.nodes[part.person1_id]["partnerships"].append({
                        "partner_id": part.person2_id,
                        "type": part.partnership_type,
                        "start_year": part.start_year,
                        "end_year": part.end_year,
                        "sequence": part.sequence_number,
                    })

                if part.person2_id in G.nodes:
                    if "partnerships" not in G.nodes[part.person2_id]:
                        G.nodes[part.person2_id]["partnerships"] = []
                    G.nodes[part.person2_id]["partnerships"].append({
                        "partner_id": part.person1_id,
                        "type": part.partnership_type,
                        "start_year": part.start_year,
                        "end_year": part.end_year,
                        "sequence": part.sequence_number,
                    })

        return G

    def _add_person_node(self, G: nx.DiGraph, person: PersonDB):
        """Add a person as a node to the graph.

        Args:
            G: NetworkX graph
            person: PersonDB object
        """
        # Build display name
        full_name = person.given_name
        if person.middle_name:
            full_name += f" {person.middle_name}"
        full_name += f" {person.surname}"
        if person.maiden_name:
            full_name += f" ({person.maiden_name})"

        # Build date string
        date_str = ""
        if person.birth_year or person.death_year:
            birth = str(person.birth_year) if person.birth_year else "?"
            death = str(person.death_year) if person.death_year else "?"
            date_str = f"{birth}-{death}"

        G.add_node(
            person.id,
            full_name=full_name,
            given_name=person.given_name,
            middle_name=person.middle_name,
            surname=person.surname,
            maiden_name=person.maiden_name,
            birth_year=person.birth_year,
            death_year=person.death_year,
            date_str=date_str,
            generation=person.generation,
            confidence=person.confidence.value if person.confidence else "uncertain",
            partnerships=[],  # Will be populated later
        )

    def _get_related_people(
        self,
        session: Session,
        root_id: int,
        max_generations: Optional[int],
        include_ancestors: bool,
        include_descendants: bool,
    ) -> Set[int]:
        """Get IDs of all people related to root person.

        Args:
            session: Database session
            root_id: Root person ID
            max_generations: Maximum generations from root
            include_ancestors: Include ancestors
            include_descendants: Include descendants

        Returns:
            Set of person IDs
        """
        related_ids = {root_id}

        if include_descendants:
            descendants = self._get_descendants(session, root_id, max_generations)
            related_ids.update(descendants)

        if include_ancestors:
            ancestors = self._get_ancestors(session, root_id, max_generations)
            related_ids.update(ancestors)

        # Also include spouses of all related people
        spouses = self._get_spouses(session, related_ids)
        related_ids.update(spouses)

        return related_ids

    def _get_descendants(
        self, session: Session, person_id: int, max_generations: Optional[int]
    ) -> Set[int]:
        """Recursively get all descendants of a person.

        Args:
            session: Database session
            person_id: Person ID
            max_generations: Maximum generations to traverse

        Returns:
            Set of descendant IDs
        """
        descendants = set()
        current_level = {person_id}
        generation = 0

        while current_level and (max_generations is None or generation < max_generations):
            # Get children of current level
            children = session.query(RelationshipDB.child_id).filter(
                RelationshipDB.parent_id.in_(current_level)
            ).all()

            child_ids = {c[0] for c in children}
            descendants.update(child_ids)
            current_level = child_ids
            generation += 1

        return descendants

    def _get_ancestors(
        self, session: Session, person_id: int, max_generations: Optional[int]
    ) -> Set[int]:
        """Recursively get all ancestors of a person.

        Args:
            session: Database session
            person_id: Person ID
            max_generations: Maximum generations to traverse

        Returns:
            Set of ancestor IDs
        """
        ancestors = set()
        current_level = {person_id}
        generation = 0

        while current_level and (max_generations is None or generation < max_generations):
            # Get parents of current level
            parents = session.query(RelationshipDB.parent_id).filter(
                RelationshipDB.child_id.in_(current_level)
            ).all()

            parent_ids = {p[0] for p in parents}
            ancestors.update(parent_ids)
            current_level = parent_ids
            generation += 1

        return ancestors

    def _get_spouses(self, session: Session, person_ids: Set[int]) -> Set[int]:
        """Get all spouses of the given people.

        Args:
            session: Database session
            person_ids: Set of person IDs

        Returns:
            Set of spouse IDs
        """
        spouses = set()

        partnerships = session.query(PartnershipDB).filter(
            (PartnershipDB.person1_id.in_(person_ids))
            | (PartnershipDB.person2_id.in_(person_ids))
        ).all()

        for part in partnerships:
            if part.person1_id in person_ids:
                spouses.add(part.person2_id)
            if part.person2_id in person_ids:
                spouses.add(part.person1_id)

        return spouses

    def get_all_surnames(self) -> List[str]:
        """Get all unique surnames in the database.

        Returns:
            Sorted list of surnames
        """
        with self.store.get_session() as session:
            surnames = session.query(PersonDB.surname).distinct().all()
            return sorted([s[0] for s in surnames if s[0]])

    def search_people(self, search_term: str) -> List[Dict]:
        """Search for people by name.

        Args:
            search_term: Search term (matches given name, middle name, or surname)
                        Supports multi-word searches (e.g., "William Troy Keenum")

        Returns:
            List of person dictionaries with id, name, and dates, sorted by relevance
        """
        with self.store.get_session() as session:
            # Split search term into words for multi-word matching
            search_words = search_term.strip().split()
            search_lower = search_term.lower()

            # For single word searches, use the optimized SQL filter
            if len(search_words) == 1:
                people = session.query(PersonDB).filter(
                    (PersonDB.given_name.ilike(f"%{search_term}%"))
                    | (PersonDB.middle_name.ilike(f"%{search_term}%"))
                    | (PersonDB.surname.ilike(f"%{search_term}%"))
                ).limit(200).all()
            else:
                # For multi-word searches, get more candidates and filter in Python
                # Build an OR filter for any field containing any word
                from sqlalchemy import or_
                word_filters = []
                for word in search_words:
                    word_filters.extend([
                        PersonDB.given_name.ilike(f"%{word}%"),
                        PersonDB.middle_name.ilike(f"%{word}%"),
                        PersonDB.surname.ilike(f"%{word}%")
                    ])
                people = session.query(PersonDB).filter(or_(*word_filters)).limit(500).all()

            results = []

            for p in people:
                # Build full name including middle name if present
                full_name_parts = [p.given_name or ""]
                if p.middle_name:
                    full_name_parts.append(p.middle_name)
                full_name_parts.append(p.surname or "")
                full_name_without_dates = " ".join(full_name_parts)

                # For multi-word search, check if all words are present in full name
                if len(search_words) > 1:
                    full_name_lower = full_name_without_dates.lower()
                    if not all(word.lower() in full_name_lower for word in search_words):
                        continue  # Skip if not all words match

                # Add birth/death years to display name
                full_name = full_name_without_dates
                if p.birth_year or p.death_year:
                    birth = str(p.birth_year) if p.birth_year else "?"
                    death = str(p.death_year) if p.death_year else "?"
                    full_name += f" ({birth}-{death})"

                # Calculate relevance score (lower is better)
                given_lower = (p.given_name or "").lower()
                middle_lower = (p.middle_name or "").lower()
                surname_lower = (p.surname or "").lower()
                full_name_lower = full_name_without_dates.lower()

                # Check for multi-word exact or starts-with match
                if len(search_words) > 1:
                    if full_name_lower == search_lower:
                        relevance = 1  # exact full name match
                    elif full_name_lower.startswith(search_lower):
                        relevance = 2  # full name starts with search
                    else:
                        relevance = 3  # all words present
                else:
                    # Single word relevance scoring
                    if given_lower == search_lower or surname_lower == search_lower:
                        relevance = 1  # exact match
                    elif given_lower.startswith(search_lower) or surname_lower.startswith(search_lower):
                        relevance = 2  # starts with
                    elif middle_lower == search_lower:
                        relevance = 3  # exact match in middle name
                    elif middle_lower.startswith(search_lower):
                        relevance = 4  # starts with in middle name
                    else:
                        relevance = 5  # contains somewhere

                results.append({
                    "id": p.id,
                    "name": full_name,
                    "given_name": p.given_name,
                    "surname": p.surname,
                    "birth_year": p.birth_year,
                    "death_year": p.death_year,
                    "relevance": relevance,
                })

            # Sort by relevance, then alphabetically by name
            results.sort(key=lambda x: (x["relevance"], x["name"]))

            return results
