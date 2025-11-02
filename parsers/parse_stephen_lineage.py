"""Parse Stephen Stone Keenum lineage from extracted text file - IMPROVED VERSION."""

import re
from typing import List, Tuple, Optional


class LineagePerson:
    """Represents a person in the lineage."""

    def __init__(self, generation: int, given_name: str, middle_name: str, surname: str,
                 maiden_name: str, birth_year: Optional[int], death_year: Optional[int],
                 is_spouse: bool, notes: str = ""):
        self.generation = generation
        self.given_name = given_name
        self.middle_name = middle_name
        self.surname = surname
        self.maiden_name = maiden_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.is_spouse = is_spouse
        self.notes = notes
        self.parent_index = None  # Will be set during parsing

    def __repr__(self):
        years = ""
        if self.birth_year and self.death_year:
            years = f" ({self.birth_year}-{self.death_year})"
        elif self.birth_year:
            years = f" ({self.birth_year}-)"
        elif self.death_year:
            years = f" (-{self.death_year})"

        spouse_marker = "+" if self.is_spouse else ""
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"Gen {self.generation}: {spouse_marker}{self.given_name}{middle} {self.surname}{years}"


def parse_name_and_dates(line: str) -> Tuple[str, str, str, str, Optional[int], Optional[int], str]:
    """
    Parse a line to extract name components and dates.

    Returns: (given_name, middle_name, surname, maiden_name, birth_year, death_year, notes)
    """
    original_line = line

    # Remove generation number at start (including ".... N" format)
    line = re.sub(r'^[.\s]*\d+\s+', '', line)

    # Remove spouse markers (. + or just +, including comma-period variations)
    line = re.sub(r'^[,\.\s]*\+\s*', '', line)

    line = line.strip()

    # Extract nickname/alias in parentheses (but NOT dates in parentheses)
    notes = ""
    # Look for text in parens that is NOT a year
    nickname_pattern = r'\(([^)]+)\)'
    for match in re.finditer(nickname_pattern, line):
        content = match.group(1)
        # If it doesn't look like a date, treat as nickname
        if not re.search(r'\d{4}', content):
            notes = content
            # Remove this from the line
            line = line[:match.start()] + ' ' + line[match.end():]
            break

    # Extract dates
    # Patterns to match:
    # - Abt. 1818 - Abt. 1880
    # - 1814-1862
    # - Abt. 1838 -1880 (note: no space after -)
    # - 1820 -
    # - - 1850
    birth_year = None
    death_year = None

    # Try to find date patterns and extract them
    # Pattern 1: Abt. YYYY - Abt. YYYY  or  Abt. YYYY -YYYY
    date_pattern1 = r'(Abt\.\s*)?(\d{4})\s*-\s*(Abt\.\s*)?(\d{4})'
    match = re.search(date_pattern1, line)
    if match:
        birth_year = int(match.group(2))
        death_year = int(match.group(4))
        # Remove the entire date portion
        line = line[:match.start()] + ' ' + line[match.end():]
    else:
        # Pattern 2: YYYY - (birth only)
        date_pattern2 = r'(Abt\.\s*)?(\d{4})\s*-\s*$'
        match = re.search(date_pattern2, line)
        if match:
            birth_year = int(match.group(2))
            line = line[:match.start()] + ' ' + line[match.end():]
        else:
            # Pattern 3: - YYYY (death only)
            date_pattern3 = r'-\s*(Abt\.\s*)?(\d{4})'
            match = re.search(date_pattern3, line)
            if match:
                death_year = int(match.group(2))
                line = line[:match.start()] + ' ' + line[match.end():]

    # Clean up extra spaces
    line = ' '.join(line.split())

    # Now parse the name
    # The line should now contain only the name
    parts = line.strip().split()

    given_name = ""
    middle_name = ""
    surname = ""
    maiden_name = ""

    if len(parts) == 0:
        return "", "", "", "", birth_year, death_year, notes

    # Common pattern: FirstName MiddleName(s) LastName
    # Assume last word is surname
    if len(parts) >= 2:
        surname = parts[-1]
        given_name = parts[0]
        # Everything between is middle name
        if len(parts) > 2:
            middle_name = " ".join(parts[1:-1])
    elif len(parts) == 1:
        # Only one name - treat as given name
        given_name = parts[0]

    # Fix common OCR errors
    given_name = given_name.replace("Maiy", "Mary")
    if middle_name:
        middle_name = middle_name.replace("Maiy", "Mary")

    return given_name, middle_name, surname, maiden_name, birth_year, death_year, notes


def parse_lineage_file(filename: str) -> List[LineagePerson]:
    """Parse the lineage file and return list of persons."""
    persons = []

    with open(filename, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines, page markers, headers, footnotes
        if not line:
            i += 1
            continue
        if line.startswith('---') or line.startswith('==='):
            i += 1
            continue
        if 'DESCEND' in line.upper() or 'PAGE' in line.upper():
            i += 1
            continue
        # Skip lines with special markers like *2nd Husband
        if line.startswith('*'):
            i += 1
            continue
        # Skip lines that are just punctuation
        if line in ['l', ',', '.', ',.', '..', ',.']:
            i += 1
            continue

        # Determine if this is a generation line or spouse line
        is_spouse = False
        current_generation = None

        # Check for generation number at start (including ".... N" format for late entries)
        # Pattern: optional dots/periods, then digit, then space
        gen_match = re.match(r'^[.\s]*(\d+)\s+', line)
        if gen_match:
            current_generation = int(gen_match.group(1))
            is_spouse = False
        # Check for spouse marker (. + or just + or ,. +)
        elif re.match(r'^[,\.\s]*\+', line):
            is_spouse = True
            # Spouse inherits generation from previous non-spouse person
            if persons:
                current_generation = persons[-1].generation
        else:
            # Unrecognized format, skip
            i += 1
            continue

        # Parse the name and dates
        given, middle, surname, maiden, birth, death, notes = parse_name_and_dates(line)

        # Skip if no valid name extracted
        if not given or not surname:
            i += 1
            continue

        person = LineagePerson(
            generation=current_generation,
            given_name=given,
            middle_name=middle,
            surname=surname,
            maiden_name=maiden,
            birth_year=birth,
            death_year=death,
            is_spouse=is_spouse,
            notes=notes
        )

        persons.append(person)
        i += 1

    return persons


def main():
    """Main function to parse and display the lineage."""
    persons = parse_lineage_file('stephen_lineage_raw.txt')

    print(f"Total persons parsed: {len(persons)}")
    print(f"\n{'='*80}")
    print("First 30 persons:")
    print('='*80)
    for i, person in enumerate(persons[:30]):
        spouse_mark = "(spouse)" if person.is_spouse else ""
        print(f"{i+1:3d}. {person} {spouse_mark}")

    # Count by generation
    gen_counts = {}
    spouse_counts = {}
    for person in persons:
        gen_counts[person.generation] = gen_counts.get(person.generation, 0) + 1
        if person.is_spouse:
            spouse_counts[person.generation] = spouse_counts.get(person.generation, 0) + 1

    print(f"\n{'='*80}")
    print("Generation counts (total / spouses):")
    print('='*80)
    for gen in sorted(gen_counts.keys()):
        spouses = spouse_counts.get(gen, 0)
        total = gen_counts[gen]
        children = total - spouses
        print(f"  Generation {gen}: {total} total ({children} children + {spouses} spouses)")

    # Verify Stephen and Mary
    print(f"\n{'='*80}")
    print("Verification of key people:")
    print('='*80)
    if len(persons) >= 2:
        stephen = persons[0]
        mary = persons[1] if len(persons) > 1 and persons[1].is_spouse else None

        print(f"\nStephen (person 0):")
        print(f"  Generation: {stephen.generation}")
        print(f"  Name: {stephen.given_name} {stephen.middle_name} {stephen.surname}")
        print(f"  Years: {stephen.birth_year}-{stephen.death_year}")
        print(f"  Is spouse: {stephen.is_spouse}")

        if mary:
            print(f"\nMary (person 1):")
            print(f"  Generation: {mary.generation}")
            print(f"  Name: {mary.given_name} {mary.middle_name} {mary.surname}")
            print(f"  Years: {mary.birth_year}-{mary.death_year}")
            print(f"  Is spouse: {mary.is_spouse}")


if __name__ == "__main__":
    main()
