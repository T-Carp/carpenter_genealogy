"""FastAPI routes for genealogy data."""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
import networkx as nx

from .dependencies import get_graph_builder, get_structured_store
from ..visualizations.graph_builder import FamilyGraphBuilder
from ..database.structured_store import StructuredStore


# ============================================================================
# Response Models (Pydantic)
# ============================================================================

class PersonResponse(BaseModel):
    """Person data response model."""
    id: int
    given_name: Optional[str] = None
    surname: Optional[str] = None
    full_name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    birth_place: Optional[str] = None
    death_place: Optional[str] = None
    gender: Optional[str] = None
    maiden_name: Optional[str] = None


class RelationshipResponse(BaseModel):
    """Relationship data response model."""
    source: int
    target: int
    relationship_type: str


class SearchResultResponse(BaseModel):
    """Search result response model."""
    id: int
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    relevance: float = 1.0


class SearchResponse(BaseModel):
    """Search response with results."""
    results: List[SearchResultResponse]
    total: int
    limit: int
    offset: int


class GraphNodeResponse(BaseModel):
    """Graph node response model."""
    id: int
    given_name: Optional[str] = None
    surname: Optional[str] = None
    full_name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    birth_place: Optional[str] = None
    death_place: Optional[str] = None
    date_str: Optional[str] = None


class GraphEdgeResponse(BaseModel):
    """Graph edge response model."""
    source: int
    target: int
    relationship_type: str


class GraphMetadataResponse(BaseModel):
    """Graph metadata response."""
    total_nodes: int
    total_edges: int
    max_depth: Optional[int] = None
    surnames: List[str]


class GraphResponse(BaseModel):
    """Complete graph response."""
    nodes: List[GraphNodeResponse]
    edges: List[GraphEdgeResponse]
    metadata: GraphMetadataResponse


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str = "1.0.0"
    database_connected: bool


class LineagePersonResponse(BaseModel):
    """Person in lineage path response model."""
    id: int
    name: str
    generation: int
    birth_year: Optional[int] = None
    death_year: Optional[int] = None


class LineagePathResponse(BaseModel):
    """Lineage path response model."""
    path: List[LineagePersonResponse]
    relationship_description: str
    generations_from_ancestor: int


class FamilyMemberResponse(BaseModel):
    """Family member response model."""
    id: int
    name: str
    relationship: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    additional_info: Optional[str] = None


class DirectFamilyResponse(BaseModel):
    """Direct family relationships response model."""
    parents: List[FamilyMemberResponse]
    siblings: List[FamilyMemberResponse]
    spouses: List[FamilyMemberResponse]
    children: List[FamilyMemberResponse]


# ============================================================================
# Router
# ============================================================================

router = APIRouter(prefix="/api")


# ============================================================================
# Health Check
# ============================================================================

@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check(
    store: StructuredStore = Depends(get_structured_store)
) -> HealthResponse:
    """Check API health and database connection.

    Returns:
        Health status
    """
    try:
        # Test database connection by counting persons
        session = store.Session()
        from ..database.structured_store import Person
        count = session.query(Person).count()
        session.close()

        return HealthResponse(
            status="healthy",
            database_connected=True
        )
    except Exception as e:
        return HealthResponse(
            status="degraded",
            database_connected=False
        )


# ============================================================================
# Genealogy Endpoints
# ============================================================================

@router.get("/genealogy/search", response_model=SearchResponse, tags=["genealogy"])
async def search_people(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Result offset"),
    builder: FamilyGraphBuilder = Depends(get_graph_builder)
) -> SearchResponse:
    """Search for people by name.

    Args:
        q: Search query (minimum 2 characters)
        limit: Maximum number of results (1-100)
        offset: Result offset for pagination

    Returns:
        Search results with metadata
    """
    try:
        # Use graph builder's search
        results = builder.search_people(q)

        # Convert to response model
        search_results = [
            SearchResultResponse(
                id=r["id"],
                name=r["name"],
                birth_year=r.get("birth_year"),
                death_year=r.get("death_year"),
                relevance=1.0  # Could add relevance scoring later
            )
            for r in results[offset:offset+limit]
        ]

        return SearchResponse(
            results=search_results,
            total=len(results),
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genealogy/surnames", response_model=List[str], tags=["genealogy"])
async def get_surnames(
    builder: FamilyGraphBuilder = Depends(get_graph_builder)
) -> List[str]:
    """Get all unique surnames in the database.

    Returns:
        List of surnames
    """
    try:
        return builder.get_all_surnames()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genealogy/person/{person_id}", response_model=PersonResponse, tags=["genealogy"])
async def get_person(
    person_id: int,
    store: StructuredStore = Depends(get_structured_store)
) -> PersonResponse:
    """Get detailed information about a specific person.

    Args:
        person_id: Person ID

    Returns:
        Person details
    """
    try:
        from ..database.structured_store import PersonDB

        with store.get_session() as session:
            person = session.query(PersonDB).filter(PersonDB.id == person_id).first()

            if not person:
                raise HTTPException(status_code=404, detail=f"Person {person_id} not found")

            # Build full name
            full_name_parts = []
            if person.given_name:
                full_name_parts.append(person.given_name)
            if person.middle_name:
                full_name_parts.append(person.middle_name)
            if person.surname:
                full_name_parts.append(person.surname)
            full_name = " ".join(full_name_parts) if full_name_parts else "Unknown"

            return PersonResponse(
                id=person.id,
                given_name=person.given_name,
                surname=person.surname,
                full_name=full_name,
                birth_year=person.birth_year,
                death_year=person.death_year,
                birth_place=None,  # Not in database
                death_place=None,  # Not in database
                gender=None,  # Not in database
                maiden_name=person.maiden_name
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genealogy/graph", response_model=GraphResponse, tags=["genealogy"])
async def get_family_graph(
    root_id: Optional[int] = Query(None, description="Root person ID"),
    generations: Optional[int] = Query(2, ge=1, le=10, description="Maximum generations"),
    include_ancestors: bool = Query(True, description="Include ancestors"),
    include_descendants: bool = Query(True, description="Include descendants"),
    surname_filter: Optional[str] = Query(None, description="Filter by surname"),
    builder: FamilyGraphBuilder = Depends(get_graph_builder)
) -> GraphResponse:
    """Get family tree graph data.

    Args:
        root_id: Root person ID (optional, returns all if not specified)
        generations: Maximum generations to include (1-10)
        include_ancestors: Include ancestors
        include_descendants: Include descendants
        surname_filter: Filter by specific surname

    Returns:
        Graph data with nodes, edges, and metadata
    """
    try:
        # Build graph using existing builder
        G = builder.build_graph(
            root_person_id=root_id,
            max_generations=generations,
            include_ancestors=include_ancestors,
            include_descendants=include_descendants,
            surname_filter=surname_filter
        )

        # Convert nodes to response format
        nodes = []
        for node_id in G.nodes:
            node_data = G.nodes[node_id]
            nodes.append(GraphNodeResponse(
                id=node_id,
                given_name=node_data.get("given_name"),
                surname=node_data.get("surname"),
                full_name=node_data.get("full_name", "Unknown"),
                birth_year=node_data.get("birth_year"),
                death_year=node_data.get("death_year"),
                birth_place=node_data.get("birth_place"),
                death_place=node_data.get("death_place"),
                date_str=node_data.get("date_str")
            ))

        # Convert edges to response format
        edges = []
        for source, target in G.edges:
            edge_data = G.edges[source, target]
            edges.append(GraphEdgeResponse(
                source=source,
                target=target,
                relationship_type=edge_data.get("relationship_type", "related_to")
            ))

        # Collect unique surnames
        surnames = set()
        for node_id in G.nodes:
            surname = G.nodes[node_id].get("surname")
            if surname:
                surnames.add(surname)

        # Create metadata
        metadata = GraphMetadataResponse(
            total_nodes=len(G.nodes),
            total_edges=len(G.edges),
            max_depth=generations,
            surnames=sorted(list(surnames))
        )

        return GraphResponse(
            nodes=nodes,
            edges=edges,
            metadata=metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genealogy/relationships/{person_id}", response_model=List[RelationshipResponse], tags=["genealogy"])
async def get_relationships(
    person_id: int,
    store: StructuredStore = Depends(get_structured_store)
) -> List[RelationshipResponse]:
    """Get all relationships for a specific person.

    Args:
        person_id: Person ID

    Returns:
        List of relationships
    """
    try:
        from ..database.structured_store import PersonDB, RelationshipDB

        with store.get_session() as session:
            # Check if person exists
            person = session.query(PersonDB).filter(PersonDB.id == person_id).first()
            if not person:
                raise HTTPException(status_code=404, detail=f"Person {person_id} not found")

            # Get all relationships where person is either parent or child
            relationships = session.query(RelationshipDB).filter(
                (RelationshipDB.parent_id == person_id) |
                (RelationshipDB.child_id == person_id)
            ).all()

            # Convert to response format
            result = []
            for rel in relationships:
                result.append(RelationshipResponse(
                    source=rel.parent_id,
                    target=rel.child_id,
                    relationship_type=rel.relationship_type
                ))

            return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genealogy/lineage/{person_id}", response_model=LineagePathResponse, tags=["genealogy"])
async def get_lineage_path(
    person_id: int,
    store: StructuredStore = Depends(get_structured_store)
) -> LineagePathResponse:
    """Get lineage path from person to their earliest Keenum ancestor.

    Args:
        person_id: Person ID

    Returns:
        Lineage path with ancestor relationship description
    """
    try:
        from ..database.structured_store import PersonDB, RelationshipDB

        with store.get_session() as session:
            # Check if person exists
            person = session.query(PersonDB).filter(PersonDB.id == person_id).first()
            if not person:
                raise HTTPException(status_code=404, detail=f"Person {person_id} not found")

            def get_parents(pid):
                """Get all parents of a person."""
                parent_rels = session.query(RelationshipDB).filter(RelationshipDB.child_id == pid).all()
                parents = []
                for rel in parent_rels:
                    parent = session.query(PersonDB).filter(PersonDB.id == rel.parent_id).first()
                    if parent:
                        parents.append(parent)
                return parents

            def find_path_to_root(pid, visited=None):
                """Recursively find all paths to root ancestors."""
                if visited is None:
                    visited = set()

                if pid in visited:
                    return []

                visited.add(pid)
                person = session.query(PersonDB).filter(PersonDB.id == pid).first()
                if not person:
                    return []

                parents = get_parents(pid)

                # If no parents, this is a root ancestor
                if not parents:
                    return [[person]]

                # Recursively find paths through each parent
                all_paths = []
                for parent in parents:
                    parent_paths = find_path_to_root(parent.id, visited.copy())
                    for path in parent_paths:
                        all_paths.append(path + [person])

                return all_paths

            # Find all paths to root ancestors
            all_paths = find_path_to_root(person_id)

            # Filter for paths that lead to Keenum ancestors
            keenum_paths = []
            for path in all_paths:
                # Check if the root (first person in path) is a Keenum
                if path and path[0].surname and 'keenum' in path[0].surname.lower():
                    keenum_paths.append(path)

            if not keenum_paths:
                raise HTTPException(status_code=404, detail="No Keenum ancestor found for this person")

            # Find the earliest Keenum ancestor (by generation, then by birth year)
            earliest_path = None
            earliest_gen = float('inf')
            earliest_birth = float('inf')

            for path in keenum_paths:
                root = path[0]
                gen = root.generation if root.generation else float('inf')
                birth = root.birth_year if root.birth_year else float('inf')

                if gen < earliest_gen or (gen == earliest_gen and birth < earliest_birth):
                    earliest_gen = gen
                    earliest_birth = birth
                    earliest_path = path

            if not earliest_path:
                raise HTTPException(status_code=404, detail="No Keenum ancestor path found")

            # Convert to response format
            lineage_persons = [
                LineagePersonResponse(
                    id=p.id,
                    name=f"{p.given_name} {p.surname}",
                    generation=p.generation or 0,
                    birth_year=p.birth_year,
                    death_year=p.death_year
                )
                for p in earliest_path
            ]

            # Calculate relationship description
            generations_from_ancestor = len(earliest_path) - 1
            if generations_from_ancestor == 0:
                relationship = "self (root ancestor)"
            elif generations_from_ancestor == 1:
                relationship = "child"
            elif generations_from_ancestor == 2:
                relationship = "grandchild"
            elif generations_from_ancestor == 3:
                relationship = "great-grandchild"
            elif generations_from_ancestor > 3:
                greats = "great-" * (generations_from_ancestor - 2)
                relationship = f"{greats}grandchild"
            else:
                relationship = "unknown"

            ancestor_name = earliest_path[0].given_name + " " + earliest_path[0].surname
            if generations_from_ancestor > 0:
                relationship_desc = f"This person is the {relationship} of {ancestor_name}"
            else:
                relationship_desc = f"This person is a root Keenum ancestor"

            return LineagePathResponse(
                path=lineage_persons,
                relationship_description=relationship_desc,
                generations_from_ancestor=generations_from_ancestor
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genealogy/family/{person_id}", response_model=DirectFamilyResponse, tags=["genealogy"])
async def get_direct_family(
    person_id: int,
    store: StructuredStore = Depends(get_structured_store)
) -> DirectFamilyResponse:
    """Get direct family relationships for a person (parents, siblings, spouses, children).

    Args:
        person_id: Person ID

    Returns:
        Direct family relationships
    """
    try:
        from ..database.structured_store import PersonDB, RelationshipDB, PartnershipDB

        with store.get_session() as session:
            # Check if person exists
            person = session.query(PersonDB).filter(PersonDB.id == person_id).first()
            if not person:
                raise HTTPException(status_code=404, detail=f"Person {person_id} not found")

            # Get parents
            parents = []
            parent_rels = session.query(RelationshipDB).filter(RelationshipDB.child_id == person_id).all()
            for rel in parent_rels:
                parent = session.query(PersonDB).filter(PersonDB.id == rel.parent_id).first()
                if parent:
                    parents.append(FamilyMemberResponse(
                        id=parent.id,
                        name=f"{parent.given_name} {parent.surname}",
                        relationship=rel.relationship_type,
                        birth_year=parent.birth_year,
                        death_year=parent.death_year
                    ))

            # Get siblings (people who share at least one parent)
            siblings = []
            if parent_rels:
                siblings_set = set()
                for parent_rel in parent_rels:
                    sibling_rels = session.query(RelationshipDB).filter(
                        RelationshipDB.parent_id == parent_rel.parent_id,
                        RelationshipDB.child_id != person_id
                    ).all()
                    for sib_rel in sibling_rels:
                        siblings_set.add(sib_rel.child_id)

                for sib_id in sorted(siblings_set):
                    sibling = session.query(PersonDB).filter(PersonDB.id == sib_id).first()
                    if sibling:
                        siblings.append(FamilyMemberResponse(
                            id=sibling.id,
                            name=f"{sibling.given_name} {sibling.surname}",
                            relationship="sibling",
                            birth_year=sibling.birth_year,
                            death_year=sibling.death_year
                        ))

            # Get spouses/partners
            spouses = []
            partnerships = session.query(PartnershipDB).filter(
                (PartnershipDB.person1_id == person_id) | (PartnershipDB.person2_id == person_id)
            ).all()

            for part in partnerships:
                other_id = part.person2_id if part.person1_id == person_id else part.person1_id
                other = session.query(PersonDB).filter(PersonDB.id == other_id).first()
                if other:
                    additional_info = []
                    if part.start_year:
                        additional_info.append(f"married {part.start_year}")
                    if part.end_year:
                        additional_info.append(f"to {part.end_year}")
                    if part.sequence_number:
                        additional_info.append(f"marriage #{part.sequence_number}")

                    spouses.append(FamilyMemberResponse(
                        id=other.id,
                        name=f"{other.given_name} {other.surname}",
                        relationship=part.partnership_type,
                        birth_year=other.birth_year,
                        death_year=other.death_year,
                        additional_info=" - ".join(additional_info) if additional_info else None
                    ))

            # Get children
            children = []
            child_rels = session.query(RelationshipDB).filter(RelationshipDB.parent_id == person_id).all()
            for rel in child_rels:
                child = session.query(PersonDB).filter(PersonDB.id == rel.child_id).first()
                if child:
                    children.append(FamilyMemberResponse(
                        id=child.id,
                        name=f"{child.given_name} {child.surname}",
                        relationship=rel.relationship_type,
                        birth_year=child.birth_year,
                        death_year=child.death_year
                    ))

            return DirectFamilyResponse(
                parents=parents,
                siblings=siblings,
                spouses=spouses,
                children=children
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
