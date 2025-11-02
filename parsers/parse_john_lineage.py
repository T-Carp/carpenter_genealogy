"""Parser for John Keenum lineage data from PDF pages 143-146."""

import re
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Person:
    """Represents a person in the lineage."""
    given_name: str
    middle_name: Optional[str]
    surname: str
    birth_year: Optional[int]
    death_year: Optional[int]
    generation: int
    is_spouse: bool
    maiden_name: Optional[str] = None


def parse_year(year_str: str) -> Optional[int]:
    """Parse a year string, handling 'Abt.' prefix."""
    if not year_str or year_str == '-':
        return None

    # Remove 'Abt.' prefix
    year_str = year_str.replace('Abt.', '').replace('Abt', '').strip()

    # Extract 4-digit year
    match = re.search(r'(\d{4})', year_str)
    if match:
        return int(match.group(1))

    return None


def parse_name_and_dates(line: str) -> tuple:
    """Parse a line to extract name and dates."""
    # Pattern: Name Year-Year or Name Year- or Name -Year
    # Examples: "John Keenum -1844", "William P Keenum 1804-"

    # Check if this is a spouse line (starts with +)
    is_spouse = line.strip().startswith('+')
    clean_line = line.replace('+', '').strip()

    # Remove generation number at start if present
    clean_line = re.sub(r'^\d+\s+', '', clean_line)

    # Extract dates pattern (handles various formats)
    dates_pattern = r'((?:Abt\.\s*)?\d{4}|-)?\s*-\s*((?:Abt\.\s*)?\d{4})?'
    dates_match = re.search(dates_pattern, clean_line)

    birth_year = None
    death_year = None
    name_part = clean_line

    if dates_match:
        # Extract years
        birth_str = dates_match.group(1)
        death_str = dates_match.group(2)

        birth_year = parse_year(birth_str) if birth_str else None
        death_year = parse_year(death_str) if death_str else None

        # Remove dates from name
        name_part = clean_line[:dates_match.start()].strip()

    # Parse name (handle middle names and special cases)
    name_parts = name_part.split()

    given_name = None
    middle_name = None
    surname = None
    maiden_name = None

    if len(name_parts) >= 2:
        given_name = name_parts[0]
        surname = name_parts[-1]

        # Middle names are everything between first and last
        if len(name_parts) > 2:
            middle_name = ' '.join(name_parts[1:-1])
    elif len(name_parts) == 1:
        given_name = name_parts[0]
        surname = "Unknown"
    else:
        given_name = "Unknown"
        surname = "Unknown"

    # Handle special cases like "? Rogers" for spouses with unknown first name
    if given_name == '?':
        given_name = "Unknown"

    return given_name, middle_name, surname, birth_year, death_year, is_spouse, maiden_name


def parse_lineage_file(filename: str) -> List[Person]:
    """Parse the lineage file and return a list of Person objects."""
    persons = []
    current_generation = 1

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        # Skip empty lines and header
        if not line.strip() or line.startswith('Descendants of'):
            continue

        # Skip comment/note lines (starting with * or ..)
        if line.strip().startswith('*') or line.strip().startswith('..'):
            continue

        # Check if this is a spouse line (starts with +)
        is_spouse_line = line.strip().startswith('+')

        # Determine generation
        gen_match = re.match(r'^(\d+)\s+', line)
        if gen_match:
            current_generation = int(gen_match.group(1))
        elif not is_spouse_line:
            # If no generation number and not a spouse, skip
            continue

        # If it's a spouse line, use current generation
        generation = current_generation

        # Parse name and dates
        given_name, middle_name, surname, birth_year, death_year, is_spouse, maiden_name = parse_name_and_dates(line)

        # Skip if we couldn't parse a valid name
        if given_name == "Unknown" and surname == "Unknown":
            continue

        person = Person(
            given_name=given_name,
            middle_name=middle_name,
            surname=surname,
            birth_year=birth_year,
            death_year=death_year,
            generation=generation,
            is_spouse=is_spouse_line,  # Use the detected spouse status
            maiden_name=maiden_name
        )

        persons.append(person)

    return persons


def main():
    """Test the parser."""
    persons = parse_lineage_file('john_lineage_raw.txt')

    print(f"Parsed {len(persons)} people\n")

    # Show summary by generation
    from collections import Counter
    gen_counts = Counter(p.generation for p in persons)

    print("People by generation:")
    for gen in sorted(gen_counts.keys()):
        count = gen_counts[gen]
        spouse_count = sum(1 for p in persons if p.generation == gen and p.is_spouse)
        print(f"  Generation {gen}: {count} people ({spouse_count} spouses)")

    # Show first few people
    print("\nFirst 10 people:")
    for i, person in enumerate(persons[:10]):
        spouse_marker = " [SPOUSE]" if person.is_spouse else ""
        print(f"{i}. Gen {person.generation}: {person.given_name} {person.middle_name or ''} {person.surname} "
              f"({person.birth_year or '?'}-{person.death_year or '?'}){spouse_marker}")


if __name__ == "__main__":
    main()
