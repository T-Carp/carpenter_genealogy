"""Populate database with George Keenum lineage from PDF page 34."""

from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import get_settings


def populate_george_lineage():
    """Populate the database with George Keenum's descendants from page 34.

    This will ADD to existing database - does not clear Richard Keenum data.
    """
    settings = get_settings()
    store = StructuredStore(settings)

    print("Populating George Keenum lineage from PDF page 34...")
    print("="*60)

    # Generation 1 - George Keenum (Root)
    print("\n=== Generation 1 (Root - George Keenum) ===")

    george_id = store.add_person(
        "George", "Keenum",
        birth_year=1789,
        death_year=1851,
        generation=1,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added George Keenum (ID: {george_id}) [~1789-1851]")

    elizabeth_id = store.add_person(
        "Elizabeth", "Stone",
        birth_year=1785,
        death_year=1857,
        generation=1,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Elizabeth Stone (ID: {elizabeth_id}) [~1785-1857]")

    store.add_partnership(george_id, elizabeth_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    print("Added partnership: George + Elizabeth")

    # Generation 2 - Children of George & Elizabeth
    print("\n=== Generation 2 (Children of George & Elizabeth) ===")

    # Stephen Stone Keenum
    stephen_id = store.add_person(
        "Stephen", "Keenum",
        middle_name="Stone",
        birth_year=1814,
        death_year=1862,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Stephen Stone Keenum (ID: {stephen_id}) [1814-1862]")
    store.add_relationship(george_id, stephen_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_id, stephen_id, "biological", ConfidenceLevel.CONFIRMED)

    mary_smith_id = store.add_person(
        "Mary", "Smith",
        birth_year=1818,
        death_year=1880,
        generation=2,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Mary (Polly) Smith (ID: {mary_smith_id}) [~1818-~1880]")
    store.add_partnership(stephen_id, mary_smith_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Milly Keenum
    milly_id = store.add_person(
        "Milly", "Keenum",
        birth_year=1816,
        death_year=1850,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Milly Keenum (ID: {milly_id}) [1816-1850]")
    store.add_relationship(george_id, milly_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_id, milly_id, "biological", ConfidenceLevel.CONFIRMED)

    joel_brooks_id = store.add_person(
        "Joel", "Brooks",
        birth_year=1809,
        generation=2,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Joel Brooks (ID: {joel_brooks_id}) [~1809-]")
    store.add_partnership(milly_id, joel_brooks_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Barsheba Keenum
    barsheba_id = store.add_person(
        "Barsheba", "Keenum",
        birth_year=1818,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Barsheba Keenum (ID: {barsheba_id}) [1818-]")
    store.add_relationship(george_id, barsheba_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_id, barsheba_id, "biological", ConfidenceLevel.CONFIRMED)

    william_buster_id = store.add_person(
        "William", "Buster",
        birth_year=1818,
        generation=2,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added William Buster (ID: {william_buster_id}) [~1818-]")
    store.add_partnership(barsheba_id, william_buster_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Berry Keenum
    berry_id = store.add_person(
        "Berry", "Keenum",
        birth_year=1820,
        death_year=1853,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Berry Keenum (ID: {berry_id}) [1820-1853]")
    store.add_relationship(george_id, berry_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_id, berry_id, "biological", ConfidenceLevel.CONFIRMED)

    sarah_duncan_id = store.add_person(
        "Sarah", "Duncan",
        birth_year=1825,
        death_year=1865,
        generation=2,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Sarah (Sally) Duncan (ID: {sarah_duncan_id}) [~1825-~1865]")
    store.add_partnership(berry_id, sarah_duncan_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Mary Keenum
    mary_keenum_id = store.add_person(
        "Mary", "Keenum",
        birth_year=1821,
        death_year=1874,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Mary Keenum (ID: {mary_keenum_id}) [1821-1874]")
    store.add_relationship(george_id, mary_keenum_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_id, mary_keenum_id, "biological", ConfidenceLevel.CONFIRMED)

    william_elder_id = store.add_person(
        "William", "Elder",
        middle_name="B",
        birth_year=1821,
        death_year=1880,
        generation=2,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added William B. Elder (ID: {william_elder_id}) [~1821-1880]")
    store.add_partnership(mary_keenum_id, william_elder_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Winney Keenum (no spouse)
    winney_id = store.add_person(
        "Winney", "Keenum",
        birth_year=1823,
        death_year=1848,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Winney Keenum (ID: {winney_id}) [1823-1848]")
    store.add_relationship(george_id, winney_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_id, winney_id, "biological", ConfidenceLevel.CONFIRMED)

    # Susan Stone Keenum
    susan_id = store.add_person(
        "Susan", "Keenum",
        middle_name="Stone",
        birth_year=1826,
        death_year=1906,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Susan Stone Keenum (ID: {susan_id}) [1826-1906]")
    store.add_relationship(george_id, susan_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_id, susan_id, "biological", ConfidenceLevel.CONFIRMED)

    george_mckenzie_id = store.add_person(
        "George", "McKenzie",
        middle_name="Washington",
        birth_year=1818,
        death_year=1907,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added George Washington McKenzie (ID: {george_mckenzie_id}) [1818-1907]")
    store.add_partnership(susan_id, george_mckenzie_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    print("\n" + "="*60)
    print("✅ George Keenum lineage populated successfully!")
    print("="*60)
    print("\nView and edit at: http://localhost:7861")
    print("\nDatabase Statistics:")

    with store.get_session() as session:
        from src.database.structured_store import PersonDB, RelationshipDB, PartnershipDB
        people_count = session.query(PersonDB).count()
        rel_count = session.query(RelationshipDB).count()
        part_count = session.query(PartnershipDB).count()

        # Count by family
        george_family = session.query(PersonDB).filter(
            PersonDB.surname == "Keenum",
            PersonDB.id >= george_id
        ).count()

        print(f"  Total People: {people_count}")
        print(f"  Total Relationships: {rel_count}")
        print(f"  Total Partnerships: {part_count}")
        print(f"\n  George Keenum family members added: 8")
        print(f"  Spouses added: 6")
        print(f"  Total added: 15")


if __name__ == "__main__":
    populate_george_lineage()
