"""Populate database with Richard Keenum lineage from PDF pages 18-19."""

from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import get_settings


def populate_richard_lineage():
    """Populate the database with Richard Keenum's descendants from pages 18-19."""
    settings = get_settings()
    store = StructuredStore(settings)

    print("Populating Richard Keenum lineage from PDF pages 18-19...")
    print("="*60)

    # Generation 1 - Richard Keenum (Root)
    print("\n=== Generation 1 (Root - Richard Keenum) ===")

    richard_id = store.add_person(
        "Richard", "Keenum",
        birth_year=1785,
        death_year=1853,
        generation=1,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Richard Keenum (ID: {richard_id}) [1785-1853]")

    nancy_id = store.add_person(
        "Nancy", "Williams",
        generation=1,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Nancy Williams (ID: {nancy_id})")

    store.add_partnership(richard_id, nancy_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)
    print("Added partnership: Richard + Nancy")

    # Generation 2 - Children of Richard & Nancy
    print("\n=== Generation 2 (Children of Richard & Nancy) ===")

    # Fanny Keenum
    fanny_id = store.add_person(
        "Fanny", "Keenum",
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Fanny Keenum (ID: {fanny_id})")
    store.add_relationship(richard_id, fanny_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_id, fanny_id, "biological", ConfidenceLevel.CONFIRMED)

    william_watson_id = store.add_person(
        "William", "Watson",
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added William Watson Sr (ID: {william_watson_id})")
    store.add_partnership(fanny_id, william_watson_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Margaret (Peggy) Keenum
    peggy_id = store.add_person(
        "Margaret", "Keenum",
        birth_year=1809,
        death_year=1872,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Margaret (Peggy) Keenum (ID: {peggy_id}) [1809-1872]")
    store.add_relationship(richard_id, peggy_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_id, peggy_id, "biological", ConfidenceLevel.CONFIRMED)

    joel_cox_id = store.add_person(
        "Joel", "Cox",
        birth_year=1802,
        death_year=1876,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Joel Cox (ID: {joel_cox_id}) [1802-1876]")
    store.add_partnership(peggy_id, joel_cox_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Elizabeth Keenum
    elizabeth_k_id = store.add_person(
        "Elizabeth", "Keenum",
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Elizabeth Keenum (ID: {elizabeth_k_id})")
    store.add_relationship(richard_id, elizabeth_k_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_id, elizabeth_k_id, "biological", ConfidenceLevel.CONFIRMED)

    eli_cox_id = store.add_person(
        "Eli", "Cox",
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Eli Cox (ID: {eli_cox_id})")
    store.add_partnership(elizabeth_k_id, eli_cox_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Frances L Keenum
    frances_id = store.add_person(
        "Frances", "Keenum",
        middle_name="L",
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Frances L Keenum (ID: {frances_id})")
    store.add_relationship(richard_id, frances_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_id, frances_id, "biological", ConfidenceLevel.CONFIRMED)

    john_lucas_id = store.add_person(
        "John", "Lucas",
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added John Lucas (ID: {john_lucas_id})")
    store.add_partnership(frances_id, john_lucas_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Catharen Keenum
    catharen_id = store.add_person(
        "Catharen", "Keenum",
        birth_year=1817,
        death_year=1880,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Catharen Keenum (ID: {catharen_id}) [1817-1880]")
    store.add_relationship(richard_id, catharen_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_id, catharen_id, "biological", ConfidenceLevel.CONFIRMED)

    # Luretta Keenum
    luretta_id = store.add_person(
        "Luretta", "Keenum",
        birth_year=1820,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Luretta Keenum (ID: {luretta_id}) [1820-]")
    store.add_relationship(richard_id, luretta_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_id, luretta_id, "biological", ConfidenceLevel.CONFIRMED)

    # James Middleton Keenum
    james_m_id = store.add_person(
        "James", "Keenum",
        middle_name="Middleton",
        birth_year=1832,
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added James Middleton Keenum (ID: {james_m_id}) [1832-]")
    store.add_relationship(richard_id, james_m_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(nancy_id, james_m_id, "biological", ConfidenceLevel.CONFIRMED)

    joanna_neff_id = store.add_person(
        "Joanna", "Neff",
        generation=2,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Joanna Neff (ID: {joanna_neff_id})")
    store.add_partnership(james_m_id, joanna_neff_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Generation 3 - Grandchildren
    print("\n=== Generation 3 (Grandchildren - Cox Family) ===")

    # Children of Peggy & Joel Cox
    martha_cox_id = store.add_person(
        "Martha", "Cox",
        birth_year=1830,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Martha Cox (ID: {martha_cox_id}) [1830-]")
    store.add_relationship(peggy_id, martha_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, martha_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    william_todd_id = store.add_person(
        "William", "Todd",
        birth_year=1825,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added William Todd (ID: {william_todd_id}) [~1825-]")
    store.add_partnership(martha_cox_id, william_todd_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    william_r_cox_id = store.add_person(
        "William", "Cox",
        middle_name="Richard",
        birth_year=1832,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added William Richard Cox (ID: {william_r_cox_id}) [1832-]")
    store.add_relationship(peggy_id, william_r_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, william_r_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    hannah_thompson_id = store.add_person(
        "Hannah", "Thompson",
        middle_name="Catharine",
        birth_year=1834,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Hannah Catharine Thompson (ID: {hannah_thompson_id}) [1834-]")
    store.add_partnership(william_r_cox_id, hannah_thompson_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    john_a_cox_id = store.add_person(
        "John", "Cox",
        middle_name="Aaron",
        birth_year=1834,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added John Aaron Cox (ID: {john_a_cox_id}) [1834-]")
    store.add_relationship(peggy_id, john_a_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, john_a_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    lydia_neff_id = store.add_person(
        "Lydia", "Neff",
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Lydia Neff (ID: {lydia_neff_id})")
    store.add_partnership(john_a_cox_id, lydia_neff_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    margaret_m_cox_id = store.add_person(
        "Margaret", "Cox",
        middle_name="M",
        birth_year=1837,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Margaret M. Cox (ID: {margaret_m_cox_id}) [1837-]")
    store.add_relationship(peggy_id, margaret_m_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, margaret_m_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    joel_cunningham_id = store.add_person(
        "Joel", "Cunningham",
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Joel Cunningham (ID: {joel_cunningham_id})")
    store.add_partnership(margaret_m_cox_id, joel_cunningham_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    catherine_cox_id = store.add_person(
        "Catherine", "Cox",
        middle_name="Frances",
        birth_year=1839,
        death_year=1921,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Catherine Frances Cox (ID: {catherine_cox_id}) [1839-1921]")
    store.add_relationship(peggy_id, catherine_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, catherine_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    john_rowe_id = store.add_person(
        "John", "Rowe",
        middle_name="Michael",
        birth_year=1834,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added John Michael Rowe (ID: {john_rowe_id}) [1834-]")
    store.add_partnership(catherine_cox_id, john_rowe_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    joel_c_cox_id = store.add_person(
        "Joel", "Cox",
        middle_name="C",
        birth_year=1842,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Joel C. Cox (ID: {joel_c_cox_id}) [~1842-]")
    store.add_relationship(peggy_id, joel_c_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, joel_c_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    amanda_cox_id = store.add_person(
        "Amanda", "Cox",
        middle_name="V",
        birth_year=1848,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Amanda V. Cox (ID: {amanda_cox_id}) [~1848-]")
    store.add_relationship(peggy_id, amanda_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cox_id, amanda_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    # Children of James Middleton & Joanna Keenum
    print("\n=== Generation 3 (Grandchildren - Keenum Family) ===")

    ami_id = store.add_person(
        "Ami", "Keenum",
        birth_year=1854,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Ami Keenum (ID: {ami_id}) [~1854-]")
    store.add_relationship(james_m_id, ami_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joanna_neff_id, ami_id, "biological", ConfidenceLevel.CONFIRMED)

    william_keenum_id = store.add_person(
        "William", "Keenum",
        birth_year=1856,
        generation=3,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added William Keenum (ID: {william_keenum_id}) [~1856-]")
    store.add_relationship(james_m_id, william_keenum_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joanna_neff_id, william_keenum_id, "biological", ConfidenceLevel.CONFIRMED)

    charles_keenum_id = store.add_person(
        "Charles", "Keenum",
        birth_year=1860,
        generation=3,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Charles Keenum (ID: {charles_keenum_id}) [1860-]")
    store.add_relationship(james_m_id, charles_keenum_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joanna_neff_id, charles_keenum_id, "biological", ConfidenceLevel.CONFIRMED)

    # Generation 4 - Great-grandchildren (Todd family)
    print("\n=== Generation 4 (Great-grandchildren - Todd Family) ===")

    floyd_todd_id = store.add_person(
        "Floyd", "Todd",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Floyd Todd (ID: {floyd_todd_id})")
    store.add_relationship(martha_cox_id, floyd_todd_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_todd_id, floyd_todd_id, "biological", ConfidenceLevel.CONFIRMED)

    george_todd_id = store.add_person(
        "George", "Todd",
        birth_year=1851,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added George Todd (ID: {george_todd_id}) [~1851-]")
    store.add_relationship(martha_cox_id, george_todd_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_todd_id, george_todd_id, "biological", ConfidenceLevel.CONFIRMED)

    angeline_higgins_id = store.add_person(
        "Angeline", "Higgins",
        birth_year=1852,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Angeline Higgins (ID: {angeline_higgins_id}) [~1852-]")
    store.add_partnership(george_todd_id, angeline_higgins_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    alexander_todd_id = store.add_person(
        "Alexander", "Todd",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Alexander Todd (ID: {alexander_todd_id})")
    store.add_relationship(martha_cox_id, alexander_todd_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_todd_id, alexander_todd_id, "biological", ConfidenceLevel.CONFIRMED)

    elizabeth_todd_id = store.add_person(
        "Elizabeth", "Todd",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Elizabeth Todd (ID: {elizabeth_todd_id})")
    store.add_relationship(martha_cox_id, elizabeth_todd_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_todd_id, elizabeth_todd_id, "biological", ConfidenceLevel.CONFIRMED)

    andrew_todd_id = store.add_person(
        "Andrew", "Todd",
        middle_name="J",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Andrew J. Todd (ID: {andrew_todd_id})")
    store.add_relationship(martha_cox_id, andrew_todd_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(william_todd_id, andrew_todd_id, "biological", ConfidenceLevel.CONFIRMED)

    # Generation 4 - Children of William Richard Cox & Hannah
    print("\n=== Generation 4 (Great-grandchildren - William Richard Cox Family) ===")

    emza_cox_id = store.add_person(
        "Emza", "Cox",
        middle_name="Harriet",
        birth_year=1854,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Emza Harriet Cox (ID: {emza_cox_id}) [1854-]")
    store.add_relationship(william_r_cox_id, emza_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(hannah_thompson_id, emza_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    frederick_cottingham_id = store.add_person(
        "Frederick", "Cottingham",
        middle_name="E",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Frederick E. Cottingham (ID: {frederick_cottingham_id})")
    store.add_partnership(emza_cox_id, frederick_cottingham_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    mary_catherine_cox_id = store.add_person(
        "Mary", "Cox",
        middle_name="Catherine",
        birth_year=1856,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Mary Catherine Cox (ID: {mary_catherine_cox_id}) [1856-]")
    store.add_relationship(william_r_cox_id, mary_catherine_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(hannah_thompson_id, mary_catherine_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    daniel_pipher_id = store.add_person(
        "Daniel", "Pipher",
        middle_name="W",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Daniel W. Pipher (ID: {daniel_pipher_id})")
    store.add_partnership(mary_catherine_cox_id, daniel_pipher_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    joel_f_cox_id = store.add_person(
        "Joel", "Cox",
        middle_name="Ferdnand",
        birth_year=1858,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Joel Ferdnand Cox (ID: {joel_f_cox_id}) [1858-]")
    store.add_relationship(william_r_cox_id, joel_f_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(hannah_thompson_id, joel_f_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    emma_johnson_id = store.add_person(
        "Emma", "Johnson",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Emma Johnson (ID: {emma_johnson_id})")
    store.add_partnership(joel_f_cox_id, emma_johnson_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    elizabeth_t_cox_id = store.add_person(
        "Elizabeth", "Cox",
        middle_name="Theretia",
        birth_year=1860,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Elizabeth Theretia Cox (ID: {elizabeth_t_cox_id}) [1860-]")
    store.add_relationship(william_r_cox_id, elizabeth_t_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(hannah_thompson_id, elizabeth_t_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    flavis_boyd_id = store.add_person(
        "Flavis", "Boyd",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Flavis Boyd (ID: {flavis_boyd_id})")
    store.add_partnership(elizabeth_t_cox_id, flavis_boyd_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    emma_m_cox_id = store.add_person(
        "Emma", "Cox",
        middle_name="Margaret",
        birth_year=1862,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Emma Margaret Cox (ID: {emma_m_cox_id}) [1862-]")
    store.add_relationship(william_r_cox_id, emma_m_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(hannah_thompson_id, emma_m_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    william_a_cox_id = store.add_person(
        "William", "Cox",
        middle_name="Allen",
        birth_year=1872,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added William Allen Cox (ID: {william_a_cox_id}) [1872-]")
    store.add_relationship(william_r_cox_id, william_a_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(hannah_thompson_id, william_a_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    hattie_ingram_id = store.add_person(
        "Hattie", "Ingram",
        middle_name="Jane",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Hattie Jane Ingram (ID: {hattie_ingram_id})")
    store.add_partnership(william_a_cox_id, hattie_ingram_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    # Generation 4 - Children of John Aaron Cox & Lydia
    print("\n=== Generation 4 (Great-grandchildren - John Aaron Cox Family) ===")

    joel_s_cox_id = store.add_person(
        "Joel", "Cox",
        middle_name="S",
        birth_year=1858,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Joel S. Cox (ID: {joel_s_cox_id}) [1858-]")
    store.add_relationship(john_a_cox_id, joel_s_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(lydia_neff_id, joel_s_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    lyddie_elliot_id = store.add_person(
        "Lyddie", "Elliot",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Lyddie Elliot (ID: {lyddie_elliot_id})")
    store.add_partnership(joel_s_cox_id, lyddie_elliot_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    martha_cox2_id = store.add_person(
        "Martha", "Cox",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Martha Cox (ID: {martha_cox2_id})")
    store.add_relationship(john_a_cox_id, martha_cox2_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(lydia_neff_id, martha_cox2_id, "biological", ConfidenceLevel.CONFIRMED)

    may_cox_id = store.add_person(
        "May", "Cox",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added May Cox (ID: {may_cox_id})")
    store.add_relationship(john_a_cox_id, may_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(lydia_neff_id, may_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    jacob_cox_id = store.add_person(
        "Jacob", "Cox",
        middle_name="H",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Jacob H. Cox (ID: {jacob_cox_id})")
    store.add_relationship(john_a_cox_id, jacob_cox_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(lydia_neff_id, jacob_cox_id, "biological", ConfidenceLevel.CONFIRMED)

    # Generation 4 - Children of Margaret M. Cox & Joel Cunningham
    print("\n=== Generation 4 (Great-grandchildren - Cunningham Family) ===")

    joel_cunningham2_id = store.add_person(
        "Joel", "Cunningham",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Joel Cunningham (child) (ID: {joel_cunningham2_id})")
    store.add_relationship(margaret_m_cox_id, joel_cunningham2_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cunningham_id, joel_cunningham2_id, "biological", ConfidenceLevel.CONFIRMED)

    mary_cunningham_id = store.add_person(
        "Mary", "Cunningham",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Mary Cunningham (ID: {mary_cunningham_id})")
    store.add_relationship(margaret_m_cox_id, mary_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cunningham_id, mary_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)

    john_cunningham_id = store.add_person(
        "John", "Cunningham",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added John Cunningham (ID: {john_cunningham_id})")
    store.add_relationship(margaret_m_cox_id, john_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cunningham_id, john_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)

    jocob_cunningham_id = store.add_person(
        "Jocob", "Cunningham",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Jocob Cunningham (ID: {jocob_cunningham_id})")
    store.add_relationship(margaret_m_cox_id, jocob_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cunningham_id, jocob_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)

    clara_cunningham_id = store.add_person(
        "Clara", "Cunningham",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Clara Cunningham (ID: {clara_cunningham_id})")
    store.add_relationship(margaret_m_cox_id, clara_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cunningham_id, clara_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)

    emma_cunningham_id = store.add_person(
        "Emma", "Cunningham",
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Emma Cunningham (ID: {emma_cunningham_id})")
    store.add_relationship(margaret_m_cox_id, emma_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(joel_cunningham_id, emma_cunningham_id, "biological", ConfidenceLevel.CONFIRMED)

    # Generation 4 - Children of Catherine Frances Cox & John Michael Rowe
    print("\n=== Generation 4 (Great-grandchildren - Rowe Family) ===")

    martha_rowe_id = store.add_person(
        "Martha", "Rowe",
        middle_name="Elizabeth",
        birth_year=1862,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Martha Elizabeth Rowe (ID: {martha_rowe_id}) [1862-]")
    store.add_relationship(catherine_cox_id, martha_rowe_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, martha_rowe_id, "biological", ConfidenceLevel.CONFIRMED)

    william_bower_id = store.add_person(
        "William", "Bower",
        middle_name="Ernest",
        birth_year=1856,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added William Ernest Bower (ID: {william_bower_id}) [1856-]")
    store.add_partnership(martha_rowe_id, william_bower_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    marv_rowe_id = store.add_person(
        "Marv", "Rowe",
        middle_name="Alica",
        birth_year=1864,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Marv Alica Rowe (ID: {marv_rowe_id}) [1864-]")
    store.add_relationship(catherine_cox_id, marv_rowe_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, marv_rowe_id, "biological", ConfidenceLevel.CONFIRMED)

    joseph_tweedy_id = store.add_person(
        "Joseph", "Tweedy",
        birth_year=1851,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Joseph Tweedy (ID: {joseph_tweedy_id}) [~1851-]")
    store.add_partnership(marv_rowe_id, joseph_tweedy_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    rosetta_rowe_id = store.add_person(
        "Rosetta", "Rowe",
        birth_year=1866,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Rosetta Rowe (ID: {rosetta_rowe_id}) [1866-]")
    store.add_relationship(catherine_cox_id, rosetta_rowe_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, rosetta_rowe_id, "biological", ConfidenceLevel.CONFIRMED)

    william_keller_id = store.add_person(
        "William", "Keller",
        middle_name="Curtis",
        birth_year=1863,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added William Curtis Keller (ID: {william_keller_id}) [~1863-]")
    store.add_partnership(rosetta_rowe_id, william_keller_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    william_h_rowe_id = store.add_person(
        "William", "Rowe",
        middle_name="Henry",
        birth_year=1869,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added William Henry Rowe (ID: {william_h_rowe_id}) [1869-]")
    store.add_relationship(catherine_cox_id, william_h_rowe_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, william_h_rowe_id, "biological", ConfidenceLevel.CONFIRMED)

    mary_wingert_id = store.add_person(
        "Mary", "Wingert",
        middle_name="Matilda",
        birth_year=1873,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Mary Matilda Wingert (ID: {mary_wingert_id}) [1873-]")
    store.add_partnership(william_h_rowe_id, mary_wingert_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    charles_rowe_id = store.add_person(
        "Charles", "Rowe",
        middle_name="Frederick",
        birth_year=1872,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Charles Frederick Rowe (ID: {charles_rowe_id}) [1872-]")
    store.add_relationship(catherine_cox_id, charles_rowe_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, charles_rowe_id, "biological", ConfidenceLevel.CONFIRMED)

    anne_taylor_id = store.add_person(
        "Anne", "Taylor",
        middle_name="E",
        birth_year=1873,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Anne E. Taylor (ID: {anne_taylor_id}) [~1873-]")
    store.add_partnership(charles_rowe_id, anne_taylor_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    margaret_rowe_id = store.add_person(
        "Margaret", "Rowe",
        middle_name="Ann Barbara",
        birth_year=1874,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Margaret Ann Barbara Rowe (ID: {margaret_rowe_id}) [1874-]")
    store.add_relationship(catherine_cox_id, margaret_rowe_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, margaret_rowe_id, "biological", ConfidenceLevel.CONFIRMED)

    seth_summers_id = store.add_person(
        "Seth", "Summers",
        middle_name="B",
        birth_year=1870,
        generation=4,
        confidence=ConfidenceLevel.LIKELY
    )
    print(f"Added Seth B. Summers (ID: {seth_summers_id}) [~1870-]")
    store.add_partnership(margaret_rowe_id, seth_summers_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    lillie_rowe_id = store.add_person(
        "Lillie", "Rowe",
        middle_name="Bell",
        birth_year=1877,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Lillie Bell Rowe (ID: {lillie_rowe_id}) [1877-]")
    store.add_relationship(catherine_cox_id, lillie_rowe_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, lillie_rowe_id, "biological", ConfidenceLevel.CONFIRMED)

    john_rowe2_id = store.add_person(
        "John", "Rowe",
        birth_year=1879,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added John Rowe (child) (ID: {john_rowe2_id}) [1879-]")
    store.add_relationship(catherine_cox_id, john_rowe2_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, john_rowe2_id, "biological", ConfidenceLevel.CONFIRMED)

    amelia_pfeifer_id = store.add_person(
        "Amelia", "Pfeifer",
        middle_name="Marie",
        birth_year=1886,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Amelia Marie Pfeifer (ID: {amelia_pfeifer_id}) [1886-]")
    store.add_partnership(john_rowe2_id, amelia_pfeifer_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    albert_rowe_id = store.add_person(
        "Albert", "Rowe",
        middle_name="Francis",
        birth_year=1883,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Albert Francis Rowe (ID: {albert_rowe_id}) [1883-]")
    store.add_relationship(catherine_cox_id, albert_rowe_id, "biological", ConfidenceLevel.CONFIRMED)
    store.add_relationship(john_rowe_id, albert_rowe_id, "biological", ConfidenceLevel.CONFIRMED)

    marie_louper_id = store.add_person(
        "Marie", "Louper",
        middle_name="Ward",
        birth_year=1885,
        generation=4,
        confidence=ConfidenceLevel.CONFIRMED
    )
    print(f"Added Marie Ward Louper (ID: {marie_louper_id}) [1885-]")
    store.add_partnership(albert_rowe_id, marie_louper_id, "marriage", confidence=ConfidenceLevel.CONFIRMED)

    print("\n" + "="*60)
    print("✅ Richard Keenum lineage populated successfully!")
    print("="*60)
    print("\nView and edit at: http://localhost:7861")
    print("\nDatabase Statistics:")

    with store.get_session() as session:
        from src.database.structured_store import PersonDB, RelationshipDB, PartnershipDB
        people_count = session.query(PersonDB).count()
        rel_count = session.query(RelationshipDB).count()
        part_count = session.query(PartnershipDB).count()
        print(f"  People: {people_count}")
        print(f"  Relationships: {rel_count}")
        print(f"  Partnerships: {part_count}")


if __name__ == "__main__":
    populate_richard_lineage()
