"""Populate database with Mary Keenum and William B. Elder lineage from PDF page 115."""

from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import get_settings


def populate_mary_lineage():
    """Populate the database with Mary Keenum and William B. Elder's descendants.

    Note: Mary Keenum (ID 85) and William B. Elder (ID 86) already exist in the database
    from the George Keenum lineage. This script adds their children, grandchildren, and
    great-grandchildren spanning 4 generations.

    Data source: PDF page 115 - "Descendants of Mary Keenum"
    """
    settings = get_settings()
    store = StructuredStore(settings)

    print("="*80)
    print("Populating Mary Keenum & William B. Elder lineage")
    print("Source: PDF page 115 - Descendants of Mary Keenum")
    print("="*80)

    # Mary Keenum (ID 85) and William B. Elder (ID 86) already exist
    mary_id = 85
    william_elder_id = 86

    # Track people added for final stats
    people_added = 0
    partnerships_added = 0
    relationships_added = 0

    # Generation 3 - Children of Mary Keenum & William B. Elder
    print("\n=== Generation 3 (Children of Mary & William Elder) ===")

    # George W. Elder (1845-1911)
    george_elder_id = store.add_person(
        "George",
        "Elder",
        middle_name="W",
        birth_year=1845,
        death_year=1911,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added George W. Elder (ID: {george_elder_id}) [1845-1911]")
    store.add_relationship(mary_id, george_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_elder_id, george_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Mary Mahan (spouse of George W. Elder)
    mary_mahan_id = store.add_person(
        "Mary",
        "Mahan",
        birth_year=1856,
        death_year=1917,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Mary Mahan (ID: {mary_mahan_id}) [1856-1917]")
    store.add_partnership(george_elder_id, mary_mahan_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # Lafayette Elder (Abt. 1850-)
    lafayette_id = store.add_person(
        "Lafayette",
        "Elder",
        birth_year=1850,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Lafayette Elder (ID: {lafayette_id}) [~1850-]")
    store.add_relationship(mary_id, lafayette_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_elder_id, lafayette_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Sarah Elizabeth Elder (Abt. 1857-)
    sarah_elder_id = store.add_person(
        "Sarah",
        "Elder",
        middle_name="Elizabeth",
        birth_year=1857,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Sarah Elizabeth Elder (ID: {sarah_elder_id}) [~1857-]")
    store.add_relationship(mary_id, sarah_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_elder_id, sarah_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # William O. Smith (spouse of Sarah Elizabeth Elder)
    william_smith_id = store.add_person(
        "William",
        "Smith",
        middle_name="O",
        birth_year=1851,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added William O. Smith (ID: {william_smith_id}) [~1851-]")
    store.add_partnership(sarah_elder_id, william_smith_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # Generation 4 - Grandchildren (Children of George W. Elder & Mary Mahan)
    print("\n=== Generation 4 (Grandchildren - Elder Family) ===")

    # Sarah (Sallie) Elder (1875-)
    sallie_elder_id = store.add_person(
        "Sarah",
        "Elder",
        birth_year=1875,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Sarah (Sallie) Elder (ID: {sallie_elder_id}) [1875-]")
    store.add_relationship(george_elder_id, sallie_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(mary_mahan_id, sallie_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Rube Chapman (spouse of Sallie Elder)
    rube_chapman_id = store.add_person(
        "Rube",
        "Chapman",
        generation=4,
        confidence=ConfidenceLevel.POSSIBLE
    )
    people_added += 1
    print(f"Added Rube Chapman (ID: {rube_chapman_id})")
    store.add_partnership(sallie_elder_id, rube_chapman_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # Margaret Evelyn Elder (1877-1959)
    margaret_elder_id = store.add_person(
        "Margaret",
        "Elder",
        middle_name="Evelyn",
        birth_year=1877,
        death_year=1959,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Margaret Evelyn Elder (ID: {margaret_elder_id}) [1877-1959]")
    store.add_relationship(george_elder_id, margaret_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(mary_mahan_id, margaret_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Sidney Curtis Ault (spouse of Margaret Evelyn Elder)
    sidney_ault_id = store.add_person(
        "Sidney",
        "Ault",
        middle_name="Curtis",
        birth_year=1876,
        death_year=1950,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Sidney Curtis Ault (ID: {sidney_ault_id}) [1876-1950]")
    store.add_partnership(margaret_elder_id, sidney_ault_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # Elizabeth M. Elder (1880-)
    elizabeth_elder_id = store.add_person(
        "Elizabeth",
        "Elder",
        middle_name="M",
        birth_year=1880,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Elizabeth M. Elder (ID: {elizabeth_elder_id}) [1880-]")
    store.add_relationship(george_elder_id, elizabeth_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(mary_mahan_id, elizabeth_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Caleb Ault (spouse of Elizabeth M. Elder)
    caleb_ault_id = store.add_person(
        "Caleb",
        "Ault",
        generation=4,
        confidence=ConfidenceLevel.POSSIBLE
    )
    people_added += 1
    print(f"Added Caleb Ault (ID: {caleb_ault_id})")
    store.add_partnership(elizabeth_elder_id, caleb_ault_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # R.W. Elder (Abt. 1882-1887)
    rw_elder_id = store.add_person(
        "R",
        "Elder",
        middle_name="W",
        birth_year=1882,
        death_year=1887,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added R.W. Elder (ID: {rw_elder_id}) [~1882-1887]")
    store.add_relationship(george_elder_id, rw_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(mary_mahan_id, rw_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # James M. Elder (1884-)
    james_elder_id = store.add_person(
        "James",
        "Elder",
        middle_name="M",
        birth_year=1884,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added James M. Elder (ID: {james_elder_id}) [1884-]")
    store.add_relationship(george_elder_id, james_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(mary_mahan_id, james_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Jennie Elder (1887-1934)
    jennie_elder_id = store.add_person(
        "Jennie",
        "Elder",
        birth_year=1887,
        death_year=1934,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Jennie Elder (ID: {jennie_elder_id}) [1887-1934]")
    store.add_relationship(george_elder_id, jennie_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(mary_mahan_id, jennie_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Julia M. Elder (1891-)
    julia_elder_id = store.add_person(
        "Julia",
        "Elder",
        middle_name="M",
        birth_year=1891,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Julia M. Elder (ID: {julia_elder_id}) [1891-]")
    store.add_relationship(george_elder_id, julia_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(mary_mahan_id, julia_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Alex O. Kilby (spouse of Julia M. Elder)
    alex_kilby_id = store.add_person(
        "Alex",
        "Kilby",
        middle_name="O",
        generation=4,
        confidence=ConfidenceLevel.POSSIBLE
    )
    people_added += 1
    print(f"Added Alex O. Kilby (ID: {alex_kilby_id})")
    store.add_partnership(julia_elder_id, alex_kilby_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # Gracy J. Elder (-1892)
    gracy_elder_id = store.add_person(
        "Gracy",
        "Elder",
        middle_name="J",
        death_year=1892,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Gracy J. Elder (ID: {gracy_elder_id}) [-1892]")
    store.add_relationship(george_elder_id, gracy_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(mary_mahan_id, gracy_elder_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Generation 4 - Grandchildren (Children of Sarah Elizabeth Elder & William O. Smith)
    print("\n=== Generation 4 (Grandchildren - Smith Family) ===")

    # Anna Smith (Abt. 1879-)
    anna_smith_id = store.add_person(
        "Anna",
        "Smith",
        birth_year=1879,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Anna Smith (ID: {anna_smith_id}) [~1879-]")
    store.add_relationship(sarah_elder_id, anna_smith_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_smith_id, anna_smith_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Generation 5 - Great-grandchildren (Children of Margaret Evelyn Elder & Sidney Curtis Ault)
    print("\n=== Generation 5 (Great-grandchildren - Ault Family) ===")

    # Leta Ann Ault (1901-)
    leta_ault_id = store.add_person(
        "Leta",
        "Ault",
        middle_name="Ann",
        birth_year=1901,
        generation=5,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Leta Ann Ault (ID: {leta_ault_id}) [1901-]")
    store.add_relationship(margaret_elder_id, leta_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sidney_ault_id, leta_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Raymond Andrew Blackett (spouse of Leta Ann Ault)
    raymond_blackett_id = store.add_person(
        "Raymond",
        "Blackett",
        middle_name="Andrew",
        generation=5,
        confidence=ConfidenceLevel.POSSIBLE
    )
    people_added += 1
    print(f"Added Raymond Andrew Blackett (ID: {raymond_blackett_id})")
    store.add_partnership(leta_ault_id, raymond_blackett_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # George Clifford Ault (1903-)
    george_ault_id = store.add_person(
        "George",
        "Ault",
        middle_name="Clifford",
        birth_year=1903,
        generation=5,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added George Clifford Ault (ID: {george_ault_id}) [1903-]")
    store.add_relationship(margaret_elder_id, george_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sidney_ault_id, george_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Myrtle Reese Kelson (spouse of George Clifford Ault)
    myrtle_kelson_id = store.add_person(
        "Myrtle",
        "Kelson",
        middle_name="Reese",
        generation=5,
        confidence=ConfidenceLevel.POSSIBLE
    )
    people_added += 1
    print(f"Added Myrtle Reese Kelson (ID: {myrtle_kelson_id})")
    store.add_partnership(george_ault_id, myrtle_kelson_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # Lelen Ether Ault (1910-)
    lelen_ault_id = store.add_person(
        "Lelen",
        "Ault",
        middle_name="Ether",
        birth_year=1910,
        generation=5,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Lelen Ether Ault (ID: {lelen_ault_id}) [1910-]")
    store.add_relationship(margaret_elder_id, lelen_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sidney_ault_id, lelen_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Jessie Ralph Warnick (spouse of Lelen Ether Ault)
    jessie_warnick_id = store.add_person(
        "Jessie",
        "Warnick",
        middle_name="Ralph",
        birth_year=1902,
        generation=5,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Jessie Ralph Warnick (ID: {jessie_warnick_id}) [1902-]")
    store.add_partnership(lelen_ault_id, jessie_warnick_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # William Clifton Ault (1910-1910) - died in infancy
    william_ault_id = store.add_person(
        "William",
        "Ault",
        middle_name="Clifton",
        birth_year=1910,
        death_year=1910,
        generation=5,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added William Clifton Ault (ID: {william_ault_id}) [1910-1910]")
    store.add_relationship(margaret_elder_id, william_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sidney_ault_id, william_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Mary Margaret Ault (1912-1912) - died in infancy
    mary_ault_id = store.add_person(
        "Mary",
        "Ault",
        middle_name="Margaret",
        birth_year=1912,
        death_year=1912,
        generation=5,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Mary Margaret Ault (ID: {mary_ault_id}) [1912-1912]")
    store.add_relationship(margaret_elder_id, mary_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sidney_ault_id, mary_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Carl Elder Ault (1915-1915) - died in infancy
    carl_ault_id = store.add_person(
        "Carl",
        "Ault",
        middle_name="Elder",
        birth_year=1915,
        death_year=1915,
        generation=5,
        confidence=ConfidenceLevel.CONFIRMED
    )
    people_added += 1
    print(f"Added Carl Elder Ault (ID: {carl_ault_id}) [1915-1915]")
    store.add_relationship(margaret_elder_id, carl_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sidney_ault_id, carl_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Earl Elder Ault (1919-)
    earl_ault_id = store.add_person(
        "Earl",
        "Ault",
        middle_name="Elder",
        birth_year=1919,
        generation=5,
        confidence=ConfidenceLevel.LIKELY
    )
    people_added += 1
    print(f"Added Earl Elder Ault (ID: {earl_ault_id}) [1919-]")
    store.add_relationship(margaret_elder_id, earl_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(sidney_ault_id, earl_ault_id, "biological", ConfidenceLevel.CONFIRMED)
    relationships_added += 2

    # Elaine Newman (spouse of Earl Elder Ault)
    elaine_newman_id = store.add_person(
        "Elaine",
        "Newman",
        generation=5,
        confidence=ConfidenceLevel.POSSIBLE
    )
    people_added += 1
    print(f"Added Elaine Newman (ID: {elaine_newman_id})")
    store.add_partnership(earl_ault_id, elaine_newman_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    partnerships_added += 1

    # Final summary
    print("\n" + "="*80)
    print("✅ Mary Keenum & William B. Elder lineage populated successfully!")
    print("="*80)
    print(f"\nAdded {people_added} people")
    print(f"Created {partnerships_added} partnerships")
    print(f"Created {relationships_added} parent-child relationships")
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
        print(f"  Mary Keenum & William B. Elder lineage (IDs 873+): {people_added} people (this run)")


if __name__ == "__main__":
    populate_mary_lineage()
