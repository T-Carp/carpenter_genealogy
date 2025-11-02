"""Populate database with John Keenum lineage using parsed data."""

from parse_john_lineage import parse_lineage_file
from src.database.structured_store import StructuredStore
from src.database.models import ConfidenceLevel
from src.utils.config import get_settings


def populate_john_lineage():
    """
    Populate the database with John Keenum's descendants.

    Note: This is a completely new Keenum lineage (John Keenum d. 1844),
    separate from the Richard and George Keenum lines.

    Generation mapping:
    - Chart Gen 1 (John) = Database Gen 1 (new root)
    - Chart Gen 2 = Database Gen 2
    - ...
    - Chart Gen 9 = Database Gen 9
    """
    settings = get_settings()
    store = StructuredStore(settings)

    print("="*80)
    print("Populating John Keenum lineage (178 people across 9 generations)")
    print("Source: PDF pages 143-146")
    print("="*80)

    # Parse the lineage file
    print("\nParsing lineage data...")
    persons = parse_lineage_file('john_lineage_raw.txt')
    print(f"Parsed {len(persons)} people")

    # Map person index to database ID
    person_id_map = {}

    # Track parent information for each generation
    # Key: generation number, Value: list of (person_db_id, person_idx, has_spouse)
    generation_parents = {}

    # Track the most recent non-spouse person and their spouse for partnership creation
    last_person_id = None
    last_person_idx = None
    last_person_gen = None

    # Process each person
    print("\nAdding people to database...")
    added_count = 0
    partnership_count = 0
    relationship_count = 0

    for i, person in enumerate(persons):
        # Calculate database generation (same as chart generation for this lineage)
        db_generation = person.generation

        # Determine confidence level based on dates
        if person.birth_year or person.death_year:
            confidence = ConfidenceLevel.CONFIRMED if person.birth_year and person.death_year else ConfidenceLevel.LIKELY
        else:
            confidence = ConfidenceLevel.POSSIBLE

        # Add person to database
        try:
            person_db_id = store.add_person(
                person.given_name,
                person.surname if person.surname else "Unknown",
                middle_name=person.middle_name if person.middle_name else None,
                birth_year=person.birth_year,
                death_year=person.death_year,
                generation=db_generation,
                confidence=confidence
            )

            person_id_map[i] = person_db_id
            added_count += 1

            # Print progress every 25 people
            if added_count % 25 == 0:
                print(f"  Added {added_count} people...")

            # Handle relationships and partnerships
            if person.is_spouse:
                # This is a spouse - create partnership with the last non-spouse person
                partner_id = None
                partner_idx = None

                # Try the immediately previous person if they're not a spouse and same generation
                if i > 0 and not persons[i-1].is_spouse and persons[i-1].generation == person.generation:
                    partner_id = person_id_map.get(i-1)
                    partner_idx = i-1
                # Otherwise, look for the last non-spouse person at this generation
                elif last_person_id and last_person_gen == person.generation:
                    partner_id = last_person_id
                    partner_idx = last_person_idx

                if partner_id:
                    store.add_partnership(
                        partner_id,
                        person_db_id,
                        "marriage",
                        confidence=ConfidenceLevel.CONFIRMED
                    )
                    partnership_count += 1

                    # Update the generation_parents to note this person has a spouse
                    target_gen = persons[partner_idx].generation if partner_idx is not None else person.generation
                    if target_gen in generation_parents:
                        for j, (pid, pidx, _) in enumerate(generation_parents[target_gen]):
                            if pid == partner_id:
                                generation_parents[target_gen][j] = (pid, pidx, True)
                                break
            else:
                # This is a child - create relationship with parent from previous generation
                parent_gen = person.generation - 1

                if parent_gen in generation_parents and generation_parents[parent_gen]:
                    # Get the most recent parent from the previous generation
                    parent_id, parent_idx, has_spouse = generation_parents[parent_gen][-1]

                    # Add relationship with parent
                    store.add_relationship(
                        parent_id,
                        person_db_id,
                        "biological",
                        ConfidenceLevel.CONFIRMED
                    )
                    relationship_count += 1

                    # Add relationship with parent's spouse if they have one
                    if has_spouse and parent_idx + 1 < len(persons) and persons[parent_idx + 1].is_spouse:
                        spouse_id = person_id_map.get(parent_idx + 1)
                        if spouse_id:
                            store.add_relationship(
                                spouse_id,
                                person_db_id,
                                "biological",
                                ConfidenceLevel.CONFIRMED
                            )
                            relationship_count += 1

                # This person becomes a potential parent for the next generation
                if person.generation not in generation_parents:
                    generation_parents[person.generation] = []
                generation_parents[person.generation].append((person_db_id, i, False))

                # Update last person tracking
                last_person_id = person_db_id
                last_person_idx = i
                last_person_gen = person.generation

        except Exception as e:
            print(f"Error adding person {i}: {person.given_name} {person.surname}: {e}")
            continue

    print(f"\n{added_count} people added successfully!")
    print(f"{partnership_count} partnerships created")
    print(f"{relationship_count} parent-child relationships created")

    # Print final statistics
    print("\n" + "="*80)
    print("✅ John Keenum lineage populated successfully!")
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
        print(f"  Milly Keenum & Joel Brooks lineage (IDs 855-872): 18 people")
        print(f"  Mary Keenum & William B. Elder lineage (IDs 873-904): 32 people")
        print(f"  Susan Stone Keenum & George McKenzie lineage (IDs 905-921): 12 people")
        print(f"  John Keenum lineage (IDs 922+): ~{added_count} people (this run)")


if __name__ == "__main__":
    populate_john_lineage()
