"""Populate database with Alexander Keenum lineage from PDF."""

from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import get_settings


def populate_lineage():
    """Populate the database with Alexander Keenum's descendants."""
    settings = get_settings()
    store = StructuredStore(settings)

    print("Populating Alexander Keenum lineage...")

    # Generation 0 - The Patriarch
    print("\n=== Generation 0 (Patriarch) ===")

    alexander_id = store.add_person(
        "Alexander", "Keenum",
        death_year=1778,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Alexander Keenum (ID: {alexander_id})")

    sarah_id = store.add_person(
        "Sarah", "Keenum",
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Sarah Keenum (ID: {sarah_id})")

    # Partnership
    store.add_partnership(alexander_id, sarah_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    print(f"Added partnership: Alexander + Sarah")

    # Generation 1 - Children of Alexander & Sarah
    print("\n=== Generation 1 (Children of Alexander & Sarah) ===")

    james_id = store.add_person(
        "James", "Keenum",
        birth_year=1756,
        death_year=1822,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added James Keenum (ID: {james_id})")
    store.add_relationship(alexander_id, james_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sarah_id, james_id, "biological", ConfidenceLevel.CONFIRMED)

    alexander2_id = store.add_person(
        "Alexander", "Keenum",
        birth_year=1762,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Alexander Keenum II (ID: {alexander2_id})")
    store.add_relationship(alexander_id, alexander2_id, "biological", ConfidenceLevel.LIKELY)
    store.add_relationship(sarah_id, alexander2_id, "biological", ConfidenceLevel.LIKELY)

    john_id = store.add_person(
        "John", "Keenum",
        birth_year=1765,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added John Keenum (ID: {john_id})")
    store.add_relationship(alexander_id, john_id, "biological", ConfidenceLevel.LIKELY)
    store.add_relationship(sarah_id, john_id, "biological", ConfidenceLevel.LIKELY)

    william_id = store.add_person(
        "William", "Keenum",
        confidence=ConfidenceLevel.POSSIBLE
    )
    print(f"Added William Keenum (ID: {william_id})")
    store.add_relationship(alexander_id, william_id, "biological", ConfidenceLevel.POSSIBLE)
    store.add_relationship(sarah_id, william_id, "biological", ConfidenceLevel.POSSIBLE)

    # James' spouse
    elizabeth_mason_id = store.add_person(
        "Elizabeth", "Mason",
        maiden_name="Dale",
        birth_year=1745,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Elizabeth Dale Mason (ID: {elizabeth_mason_id})")
    store.add_partnership(james_id, elizabeth_mason_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Generation 2 - Children of James & Elizabeth
    print("\n=== Generation 2 (Children of James & Elizabeth) ===")

    richard_id = store.add_person(
        "Richard", "Keenum",
        birth_year=1785,
        death_year=1853,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Richard Keenum (ID: {richard_id})")
    store.add_relationship(james_id, richard_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_mason_id, richard_id, "biological", ConfidenceLevel.CONFIRMED)

    george_id = store.add_person(
        "George", "Keenum",
        birth_year=1789,
        death_year=1851,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added George Keenum (ID: {george_id})")
    store.add_relationship(james_id, george_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(elizabeth_mason_id, george_id, "biological", ConfidenceLevel.CONFIRMED)

    # Spouses of Generation 2
    nancy_williams_id = store.add_person(
        "Nancy", "Williams",
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Nancy Williams (ID: {nancy_williams_id})")
    store.add_partnership(richard_id, nancy_williams_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    elizabeth_stone_id = store.add_person(
        "Elizabeth", "Stone",
        birth_year=1785,
        death_year=1857,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Elizabeth Stone (ID: {elizabeth_stone_id})")
    store.add_partnership(george_id, elizabeth_stone_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Generation 3 - Children of Richard & Nancy
    print("\n=== Generation 3 (Some children of Richard & Nancy) ===")

    fanny_id = store.add_person(
        "Fanny", "Keenum",
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Fanny Keenum (ID: {fanny_id})")
    store.add_relationship(richard_id, fanny_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_williams_id, fanny_id, "biological", ConfidenceLevel.CONFIRMED)

    peggy_id = store.add_person(
        "Margaret", "Keenum",
        birth_year=1809,
        death_year=1872,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Margaret (Peggy) Keenum (ID: {peggy_id})")
    store.add_relationship(richard_id, peggy_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_williams_id, peggy_id, "biological", ConfidenceLevel.CONFIRMED)

    elizabeth_keenum_id = store.add_person(
        "Elizabeth", "Keenum",
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Elizabeth Keenum (ID: {elizabeth_keenum_id})")
    store.add_relationship(richard_id, elizabeth_keenum_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_williams_id, elizabeth_keenum_id, "biological", ConfidenceLevel.CONFIRMED)

    frances_id = store.add_person(
        "Frances", "Keenum",
        middle_name="L",
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Frances L Keenum (ID: {frances_id})")
    store.add_relationship(richard_id, frances_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_williams_id, frances_id, "biological", ConfidenceLevel.CONFIRMED)

    catharen_id = store.add_person(
        "Catharen", "Keenum",
        birth_year=1817,
        death_year=1880,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Catharen Keenum (ID: {catharen_id})")
    store.add_relationship(richard_id, catharen_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_williams_id, catharen_id, "biological", ConfidenceLevel.CONFIRMED)

    luretta_id = store.add_person(
        "Luretta", "Keenum",
        birth_year=1820,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Luretta Keenum (ID: {luretta_id})")
    store.add_relationship(richard_id, luretta_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_williams_id, luretta_id, "biological", ConfidenceLevel.CONFIRMED)

    james_m_id = store.add_person(
        "James", "Keenum",
        middle_name="Middleton",
        birth_year=1832,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added James Middleton Keenum (ID: {james_m_id})")
    store.add_relationship(richard_id, james_m_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_williams_id, james_m_id, "biological", ConfidenceLevel.CONFIRMED)

    # Some spouses for Generation 3
    william_watson_id = store.add_person(
        "William", "Watson",
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added William Watson Sr (ID: {william_watson_id})")
    store.add_partnership(fanny_id, william_watson_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    joel_cox_id = store.add_person(
        "Joel", "Cox",
        birth_year=1802,
        death_year=1876,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Joel Cox (ID: {joel_cox_id})")
    store.add_partnership(peggy_id, joel_cox_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    eli_cox_id = store.add_person(
        "Eli", "Cox",
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Eli Cox (ID: {eli_cox_id})")
    store.add_partnership(elizabeth_keenum_id, eli_cox_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    john_lucas_id = store.add_person(
        "John", "Lucas",
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added John Lucas (ID: {john_lucas_id})")
    store.add_partnership(frances_id, john_lucas_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    joanna_neff_id = store.add_person(
        "Joanna", "Neff",
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Joanna Neff (ID: {joanna_neff_id})")
    store.add_partnership(james_m_id, joanna_neff_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Generation 4 - Some children of Peggy & Joel Cox
    print("\n=== Generation 4 (Sample: Children of Peggy & Joel Cox) ===")

    martha_cox_id = store.add_person(
        "Martha", "Cox",
        birth_year=1830,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Martha Cox (ID: {martha_cox_id})")
    store.add_relationship(peggy_id, martha_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, martha_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    william_r_cox_id = store.add_person(
        "William", "Cox",
        middle_name="Richard",
        birth_year=1832,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added William Richard Cox (ID: {william_r_cox_id})")
    store.add_relationship(peggy_id, william_r_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, william_r_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    john_a_cox_id = store.add_person(
        "John", "Cox",
        middle_name="Aaron",
        birth_year=1834,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added John Aaron Cox (ID: {john_a_cox_id})")
    store.add_relationship(peggy_id, john_a_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, john_a_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    margaret_m_cox_id = store.add_person(
        "Margaret", "Cox",
        middle_name="M",
        birth_year=1837,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Margaret M Cox (ID: {margaret_m_cox_id})")
    store.add_relationship(peggy_id, margaret_m_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, margaret_m_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    catherine_cox_id = store.add_person(
        "Catherine", "Cox",
        middle_name="Frances",
        birth_year=1839,
        death_year=1921,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Catherine Frances Cox (ID: {catherine_cox_id})")
    store.add_relationship(peggy_id, catherine_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, catherine_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    # Children of James Middleton Keenum & Joanna Neff
    print("\n=== Generation 4 (Children of James M & Joanna Keenum) ===")

    ami_id = store.add_person(
        "Ami", "Keenum",
        birth_year=1854,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Ami Keenum (ID: {ami_id})")
    store.add_relationship(james_m_id, ami_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joanna_neff_id, ami_id, "biological", ConfidenceLevel.CONFIRMED)

    william_keenum_id = store.add_person(
        "William", "Keenum",
        birth_year=1856,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added William Keenum (ID: {william_keenum_id})")
    store.add_relationship(james_m_id, william_keenum_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joanna_neff_id, william_keenum_id, "biological", ConfidenceLevel.CONFIRMED)

    charles_id = store.add_person(
        "Charles", "Keenum",
        birth_year=1860,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Charles Keenum (ID: {charles_id})")
    store.add_relationship(james_m_id, charles_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joanna_neff_id, charles_id, "biological", ConfidenceLevel.CONFIRMED)

    print("\n" + "="*60)
    print("✅ Database populated with initial Alexander Keenum lineage!")
    print("="*60)
    print("\nView and edit at: http://localhost:7861")
    print("\nStatistics:")
    with store.get_session() as session:
        from src.database.structured_store import PersonDB, RelationshipDB, PartnershipDB
        people_count = session.query(PersonDB).count()
        rel_count = session.query(RelationshipDB).count()
        part_count = session.query(PartnershipDB).count()
        print(f"  People: {people_count}")
        print(f"  Relationships: {rel_count}")
        print(f"  Partnerships: {part_count}")


if __name__ == "__main__":
    populate_lineage()
