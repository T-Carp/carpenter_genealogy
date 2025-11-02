"""Populate database with Berry Keenum and Sarah Duncan lineage from PDF pages 110-111."""

from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import get_settings


def populate_berry_lineage():
    """Populate the database with Berry Keenum and Sarah Duncan's descendants.

    Note: Berry Keenum (ID 83) and Sarah Duncan (ID 84) already exist in the database
    from the George Keenum lineage. This script adds their children and grandchildren.

    Historical note: Berry was involved in the Cherokee Removal ("Trail of Tears")
    in 1837-1838 as part of Tennessee Mounted Volunteers.
    """
    settings = get_settings()
    store = StructuredStore(settings)

    print("="*80)
    print("Populating Berry Keenum & Sarah Duncan lineage (13 people across 2 generations)")
    print("="*80)

    # Berry Keenum (ID 83) and Sarah Duncan (ID 84) already exist
    berry_id = 83
    sarah_id = 84

    # Generation 3 - Children of Berry & Sarah
    print("\n=== Generation 3 (Children of Berry & Sarah Duncan Keenum) ===")

    # Mary Elizabeth (Betsy) Keenum
    mary_elizabeth_id = store.add_person(
        "Mary",
        "Keenum",
        middle_name="Elizabeth",
        birth_year=1844,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Mary Elizabeth (Betsy) Keenum (ID: {mary_elizabeth_id}) [~1844-]")
    store.add_relationship(berry_id, mary_elizabeth_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sarah_id, mary_elizabeth_id, "biological", ConfidenceLevel.CONFIRMED)

    william_carr_id = store.add_person(
        "William",
        "Carr",
        birth_year=1844,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added William Carr (ID: {william_carr_id}) [~1844-]")
    store.add_partnership(mary_elizabeth_id, william_carr_id, "marriage",
                         confidence=ConfidenceLevel.CONFIRMED)

    # Susan Frances Keenum
    susan_frances_id = store.add_person(
        "Susan",
        "Keenum",
        middle_name="Frances",
        birth_year=1847,
        death_year=1932,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Susan Frances Keenum (ID: {susan_frances_id}) [1847-1932]")
    store.add_relationship(berry_id, susan_frances_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sarah_id, susan_frances_id, "biological", ConfidenceLevel.CONFIRMED)

    george_mcmunn_id = store.add_person(
        "George",
        "McMunn",
        middle_name="Stewart",
        death_year=1914,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added George Stewart McMunn (ID: {george_mcmunn_id}) [-1914]")
    store.add_partnership(susan_frances_id, george_mcmunn_id, "marriage",
                         start_year=1869, confidence=ConfidenceLevel.CONFIRMED)

    # Nancy Ann (Eveline) Keenum
    nancy_ann_id = store.add_person(
        "Nancy",
        "Keenum",
        middle_name="Ann",
        birth_year=1849,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Nancy Ann (Eveline) Keenum (ID: {nancy_ann_id}) [~1849-]")
    store.add_relationship(berry_id, nancy_ann_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sarah_id, nancy_ann_id, "biological", ConfidenceLevel.CONFIRMED)

    john_mcginnis_id = store.add_person(
        "John",
        "McGinnis",
        birth_year=1849,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added John McGinnis (ID: {john_mcginnis_id}) [~1849-]")
    store.add_partnership(nancy_ann_id, john_mcginnis_id, "marriage",
                         confidence=ConfidenceLevel.CONFIRMED)

    # Generation 4 - Grandchildren
    print("\n=== Generation 4 (Grandchildren - McMunn Family) ===")

    # Children of Susan Frances Keenum & George Stewart McMunn
    ella_mcmunn_id = store.add_person(
        "Ella",
        "McMunn",
        birth_year=1870,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Ella McMunn (ID: {ella_mcmunn_id}) [~1870-]")
    store.add_relationship(susan_frances_id, ella_mcmunn_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mcmunn_id, ella_mcmunn_id, "biological", ConfidenceLevel.CONFIRMED)

    jene_mcmunn_id = store.add_person(
        "Jene",
        "McMunn",
        birth_year=1872,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Jene McMunn (ID: {jene_mcmunn_id}) [~1872-]")
    store.add_relationship(susan_frances_id, jene_mcmunn_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mcmunn_id, jene_mcmunn_id, "biological", ConfidenceLevel.CONFIRMED)

    # Jene's spouse (surname Courteau)
    courteau_id = store.add_person(
        "Unknown",
        "Courteau",
        birth_year=1872,
        generation=4,
        confidence=ConfidenceLevel.POSSIBLE
    )
    print(f"Added [Unknown] Courteau (ID: {courteau_id}) [~1872-]")
    store.add_partnership(jene_mcmunn_id, courteau_id, "marriage",
                         confidence=ConfidenceLevel.LIKELY)

    florence_mcmunn_id = store.add_person(
        "Florence",
        "McMunn",
        birth_year=1875,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Florence McMunn (ID: {florence_mcmunn_id}) [~1875-]")
    store.add_relationship(susan_frances_id, florence_mcmunn_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(george_mcmunn_id, florence_mcmunn_id, "biological", ConfidenceLevel.CONFIRMED)

    # Florence's spouse (surname Matthes)
    matthes_id = store.add_person(
        "Unknown",
        "Matthes",
        birth_year=1875,
        generation=4,
        confidence=ConfidenceLevel.POSSIBLE
    )
    print(f"Added [Unknown] Matthes (ID: {matthes_id}) [~1875-]")
    store.add_partnership(florence_mcmunn_id, matthes_id, "marriage",
                         confidence=ConfidenceLevel.LIKELY)

    # Children of Nancy Ann Keenum & John McGinnis
    print("\n=== Generation 4 (Grandchildren - McGinnis Family) ===")

    lula_mcginnis_id = store.add_person(
        "Lula",
        "McGinnis",
        birth_year=1870,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Lula McGinnis (ID: {lula_mcginnis_id}) [~1870-]")
    store.add_relationship(nancy_ann_id, lula_mcginnis_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_mcginnis_id, lula_mcginnis_id, "biological", ConfidenceLevel.CONFIRMED)

    john_mcginnis_jr_id = store.add_person(
        "John",
        "McGinnis",
        birth_year=1872,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added John McGinnis (son) (ID: {john_mcginnis_jr_id}) [~1872-]")
    store.add_relationship(nancy_ann_id, john_mcginnis_jr_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_mcginnis_id, john_mcginnis_jr_id, "biological", ConfidenceLevel.CONFIRMED)

    print("\n" + "="*80)
    print("✅ Berry Keenum & Sarah Duncan lineage populated successfully!")
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
        print(f"  Milly Keenum & Joel Brooks lineage (IDs 855-870): 16 people")
        print(f"  Berry Keenum & Sarah Duncan lineage (IDs 871+): 13 people (this run)")


if __name__ == "__main__":
    populate_berry_lineage()
