"""Populate database with Susan Stone Keenum and George Washington McKenzie lineage from PDF page 120."""

from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import get_settings


def populate_susan_lineage():
    """Populate the database with Susan Stone Keenum and George Washington McKenzie's descendants.

    Note: Susan Stone Keenum (ID 88) and George Washington McKenzie (ID 89) already exist
    in the database from the George Keenum lineage. This script adds their 12 children.

    Data source: PDF page 120 - "Descendants of Susan Stone Keenum"
    """
    settings = get_settings()
    store = StructuredStore(settings)

    print("="*80)
    print("Populating Susan Stone Keenum & George Washington McKenzie lineage")
    print("Source: PDF page 120 - Descendants of Susan Stone Keenum")
    print("="*80)

    # Susan Stone Keenum (ID 88) and George Washington McKenzie (ID 89) already exist
    susan_id = 88
    george_mckenzie_id = 89

    # Track people added for final stats
    people_added = 0
    relationships_added = 0

    # Generation 3 - Children of Susan Stone Keenum & George Washington McKenzie
    print("\n=== Generation 3 (Children of Susan & George McKenzie) ===")

    # Andrew Jackson McKenzie (1844-1861)
    andrew_id = store.add_person(
        "Andrew",
        "McKenzie",
        middle_name="Jackson",
        birth_year=1844,
        death_year=1861,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Andrew Jackson McKenzie (ID: {andrew_id}) [1844-1861]")
    store.add_relationship(susan_id, andrew_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, andrew_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Alfred Benjamin McKenzie (1846-1865)
    alfred_id = store.add_person(
        "Alfred",
        "McKenzie",
        middle_name="Benjamin",
        birth_year=1846,
        death_year=1865,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Alfred Benjamin McKenzie (ID: {alfred_id}) [1846-1865]")
    store.add_relationship(susan_id, alfred_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, alfred_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Elizabeth Frische McKenzie (1849-1932)
    elizabeth_id = store.add_person(
        "Elizabeth",
        "McKenzie",
        middle_name="Frische",
        birth_year=1849,
        death_year=1932,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Elizabeth Frische McKenzie (ID: {elizabeth_id}) [1849-1932]")
    store.add_relationship(susan_id, elizabeth_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, elizabeth_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Julia Ann McKenzie (1851-1918)
    julia_id = store.add_person(
        "Julia",
        "McKenzie",
        middle_name="Ann",
        birth_year=1851,
        death_year=1918,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Julia Ann McKenzie (ID: {julia_id}) [1851-1918]")
    store.add_relationship(susan_id, julia_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, julia_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Benjamin Franklin McKenzie (1854-1924)
    benjamin_id = store.add_person(
        "Benjamin",
        "McKenzie",
        middle_name="Franklin",
        birth_year=1854,
        death_year=1924,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Benjamin Franklin McKenzie (ID: {benjamin_id}) [1854-1924]")
    store.add_relationship(susan_id, benjamin_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, benjamin_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Mary Tennessee McKenzie (1856-1935)
    mary_id = store.add_person(
        "Mary",
        "McKenzie",
        middle_name="Tennessee",
        birth_year=1856,
        death_year=1935,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Mary Tennessee McKenzie (ID: {mary_id}) [1856-1935]")
    store.add_relationship(susan_id, mary_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, mary_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Reuben Nicholson McKenzie (1858-1939)
    reuben_id = store.add_person(
        "Reuben",
        "McKenzie",
        middle_name="Nicholson",
        birth_year=1858,
        death_year=1939,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Reuben Nicholson McKenzie (ID: {reuben_id}) [1858-1939]")
    store.add_relationship(susan_id, reuben_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, reuben_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # George Calhoun McKenzie (1861-1938)
    george_jr_id = store.add_person(
        "George",
        "McKenzie",
        middle_name="Calhoun",
        birth_year=1861,
        death_year=1938,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added George Calhoun McKenzie (ID: {george_jr_id}) [1861-1938]")
    store.add_relationship(susan_id, george_jr_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, george_jr_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # James Adkins McKenzie (1865-1945)
    james_id = store.add_person(
        "James",
        "McKenzie",
        middle_name="Adkins",
        birth_year=1865,
        death_year=1945,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added James Adkins McKenzie (ID: {james_id}) [1865-1945]")
    store.add_relationship(susan_id, james_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, james_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Robert Lee McKenzie (1867-1934)
    robert_id = store.add_person(
        "Robert",
        "McKenzie",
        middle_name="Lee",
        birth_year=1867,
        death_year=1934,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Robert Lee McKenzie (ID: {robert_id}) [1867-1934]")
    store.add_relationship(susan_id, robert_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, robert_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Joseph Johnson McKenzie (1870-1870) - died in infancy
    joseph_id = store.add_person(
        "Joseph",
        "McKenzie",
        middle_name="Johnson",
        birth_year=1870,
        death_year=1870,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Joseph Johnson McKenzie (ID: {joseph_id}) [1870-1870]")
    store.add_relationship(susan_id, joseph_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, joseph_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # William Washington McKenzie (1872-1872) - died in infancy
    william_id = store.add_person(
        "William",
        "McKenzie",
        middle_name="Washington",
        birth_year=1872,
        death_year=1872,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added William Washington McKenzie (ID: {william_id}) [1872-1872]")
    store.add_relationship(susan_id, william_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mckenzie_id, william_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Final summary
    print("\n" + "="*80)
    print("✅ Susan Stone Keenum & George Washington McKenzie lineage populated!")
    print("="*80)
    print(f"\nAdded {people_added} people")
    print(f"Created {relationships_added} parent-child relationships")
    print("\nNote: 2 children (Joseph and William) died in infancy")
    print("\nView and edit at: http://localhost:7861")
    print("\nDatabase Statistics:")

    with store.get_session() as session:
        from src.database.structured_store import PersonDB, RelationshipDB, PartnershipDB
        total_people = session.query(PersonDB).count()
        total_relationships = session.query(RelationshipDB).count()
        total_partnerships = session.query(PartnershipDB).count()

        print(f"  Total People: {total_people}")
        print(f"  Total Relationships: {total_relationships}")
        print(f"  Total Partnerships: {total_partnerships}")

        print(f"\n  Richard Keenum lineage (IDs 1-74): 74 people")
        print(f"  George Keenum lineage (IDs 75-89): 15 people")
        print(f"  Stephen Stone Keenum lineage (IDs 90-854): 765 people")
        print(f"  Milly Keenum & Joel Brooks lineage (IDs 855-872): 18 people")
        print(f"  Mary Keenum & William B. Elder lineage (IDs 873-904): 32 people")
        print(f"  Susan Stone Keenum & George McKenzie lineage (IDs 905+): {people_added} people (this run)")


if __name__ == "__main__":
    populate_susan_lineage()
