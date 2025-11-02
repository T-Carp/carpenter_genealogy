"""Populate database with Milly Keenum and Joel Brooks lineage from PDF pages 105-106."""

from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import get_settings


def populate_milly_lineage():
    """Populate the database with Milly Keenum and Joel Brooks' descendants.

    Note: Milly Keenum (ID 79) and Joel Brooks (ID 80) already exist in the database
    from the George Keenum lineage. This script adds their children and grandchildren.
    """
    settings = get_settings()
    store = StructuredStore(settings)

    print("="*80)
    print("Populating Milly Keenum & Joel Brooks lineage (18 people across 2 generations)")
    print("="*80)

    # Milly Keenum (ID 79) and Joel Brooks (ID 80) already exist
    milly_id = 79
    joel_id = 80

    # Generation 3 - Children of Milly & Joel Brooks
    print("\n=== Generation 3 (Children of Milly & Joel Brooks) ===")

    # Mary Elizabeth Brooks
    mary_elizabeth_id = store.add_person(
        "Mary",
        "Brooks",
        middle_name="Elizabeth",
        birth_year=1832,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Mary Elizabeth Brooks (ID: {mary_elizabeth_id}) [1832-]")
    store.add_relationship(milly_id, mary_elizabeth_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_id, mary_elizabeth_id, "biological", ConfidenceLevel.CONFIRMED)

    thomas_white_id = store.add_person(
        "Thomas",
        "White",
        middle_name="Newton",
        birth_year=1829,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Thomas Newton White (ID: {thomas_white_id}) [~1829-]")
    store.add_partnership(mary_elizabeth_id, thomas_white_id, "marriage",
                         start_year=1850, confidence=ConfidenceLevel.CONFIRMED)

    # George F. Brooks
    george_brooks_id = store.add_person(
        "George",
        "Brooks",
        middle_name="F",
        birth_year=1835,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added George F. Brooks (ID: {george_brooks_id}) [~1835-]")
    store.add_relationship(milly_id, george_brooks_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_id, george_brooks_id, "biological", ConfidenceLevel.CONFIRMED)

    nancy_e_id = store.add_person(
        "Nancy",
        "Brooks",
        middle_name="E",
        maiden_name="Unknown",
        birth_year=1836,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Nancy E. (ID: {nancy_e_id}) [~1836-]")
    store.add_partnership(george_brooks_id, nancy_e_id, "marriage",
                         confidence=ConfidenceLevel.CONFIRMED)

    # Perlina Brooks
    perlina_id = store.add_person(
        "Perlina",
        "Brooks",
        birth_year=1837,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Perlina Brooks (ID: {perlina_id}) [~1837-]")
    store.add_relationship(milly_id, perlina_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_id, perlina_id, "biological", ConfidenceLevel.CONFIRMED)

    william_stoner_id = store.add_person(
        "William",
        "Stoner",
        birth_year=1837,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added William Stoner (ID: {william_stoner_id}) [~1837-]")
    store.add_partnership(perlina_id, william_stoner_id, "marriage",
                         confidence=ConfidenceLevel.CONFIRMED)

    # William Franklin Brooks
    william_brooks_id = store.add_person(
        "William",
        "Brooks",
        middle_name="Franklin",
        birth_year=1839,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added William Franklin Brooks (ID: {william_brooks_id}) [~1839-]")
    store.add_relationship(milly_id, william_brooks_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_id, william_brooks_id, "biological", ConfidenceLevel.CONFIRMED)

    elizabeth_nowlin_id = store.add_person(
        "Elizabeth",
        "Nowlin",
        birth_year=1855,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Elizabeth Nowlin (ID: {elizabeth_nowlin_id}) [~1855-]")
    store.add_partnership(william_brooks_id, elizabeth_nowlin_id, "marriage",
                         start_year=1874, confidence=ConfidenceLevel.CONFIRMED)

    # Jane Brooks (no spouse)
    jane_id = store.add_person(
        "Jane",
        "Brooks",
        birth_year=1840,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Jane Brooks (ID: {jane_id}) [~1840-]")
    store.add_relationship(milly_id, jane_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_id, jane_id, "biological", ConfidenceLevel.CONFIRMED)

    # Susan E. Brooks (no spouse)
    susan_id = store.add_person(
        "Susan",
        "Brooks",
        middle_name="E",
        birth_year=1844,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Susan E. Brooks (ID: {susan_id}) [~1844-]")
    store.add_relationship(milly_id, susan_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_id, susan_id, "biological", ConfidenceLevel.CONFIRMED)

    # James Worth Brooks (no spouse)
    james_id = store.add_person(
        "James",
        "Brooks",
        middle_name="Worth",
        birth_year=1847,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added James Worth Brooks (ID: {james_id}) [~1847-]")
    store.add_relationship(milly_id, james_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_id, james_id, "biological", ConfidenceLevel.CONFIRMED)

    # Generation 4 - Grandchildren
    print("\n=== Generation 4 (Grandchildren - White Family) ===")

    # Children of Mary Elizabeth Brooks & Thomas Newton White
    margaret_white_id = store.add_person(
        "Margaret",
        "White",
        middle_name="O",
        birth_year=1852,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Margaret O. White (ID: {margaret_white_id}) [~1852-]")
    store.add_relationship(mary_elizabeth_id, margaret_white_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(thomas_white_id, margaret_white_id, "biological", ConfidenceLevel.CONFIRMED)

    sarah_white_id = store.add_person(
        "Sarah",
        "White",
        middle_name="A",
        birth_year=1854,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Sarah A. White (ID: {sarah_white_id}) [~1854-]")
    store.add_relationship(mary_elizabeth_id, sarah_white_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(thomas_white_id, sarah_white_id, "biological", ConfidenceLevel.CONFIRMED)

    jane_white_id = store.add_person(
        "Jane",
        "White",
        middle_name="C",
        birth_year=1856,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Jane C. White (ID: {jane_white_id}) [~1856-]")
    store.add_relationship(mary_elizabeth_id, jane_white_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(thomas_white_id, jane_white_id, "biological", ConfidenceLevel.CONFIRMED)

    ann_white_id = store.add_person(
        "Ann",
        "White",
        middle_name="E",
        birth_year=1858,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Ann E. White (ID: {ann_white_id}) [~1858-]")
    store.add_relationship(mary_elizabeth_id, ann_white_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(thomas_white_id, ann_white_id, "biological", ConfidenceLevel.CONFIRMED)

    # Children of George F. Brooks & Nancy E.
    print("\n=== Generation 4 (Grandchildren - Brooks Family) ===")

    john_brooks_id = store.add_person(
        "John",
        "Brooks",
        birth_year=1854,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added John Brooks (ID: {john_brooks_id}) [~1854-]")
    store.add_relationship(george_brooks_id, john_brooks_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_e_id, john_brooks_id, "biological", ConfidenceLevel.CONFIRMED)

    print("\n" + "="*80)
    print("✅ Milly Keenum & Joel Brooks lineage populated successfully!")
    print("="*80)
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
        print(f"  Milly Keenum & Joel Brooks lineage (IDs 855+): 18 people (this run)")


if __name__ == "__main__":
    populate_milly_lineage()
