"""Interactive tool for entering and verifying genealogy data."""

import gradio as gr
import pandas as pd
from pathlib import Path
from typing import Optional, Tuple

from src.database.structured_store import StructuredStore, PersonDB, RelationshipDB, PartnershipDB
from src.database.models import Person, Relationship, Partnership, ConfidenceLevel
from src.utils.config import get_settings


class GenealogyDataEntry:
    """Interactive data entry tool for genealogy information."""

    def __init__(self):
        self.settings = get_settings()
        self.store = StructuredStore(self.settings)

    def get_all_people_df(self, given_name_filter: str = "", surname_filter: str = "") -> pd.DataFrame:
        """Get all people as a DataFrame for display.

        Args:
            given_name_filter: Filter by given name (case-insensitive partial match)
            surname_filter: Filter by surname (case-insensitive partial match)
        """
        with self.store.get_session() as session:
            query = session.query(PersonDB)

            # Apply filters if provided
            if given_name_filter.strip():
                query = query.filter(PersonDB.given_name.ilike(f"%{given_name_filter.strip()}%"))
            if surname_filter.strip():
                query = query.filter(PersonDB.surname.ilike(f"%{surname_filter.strip()}%"))

            people = query.order_by(PersonDB.generation, PersonDB.surname, PersonDB.given_name).all()

            if not people:
                return pd.DataFrame(columns=["ID", "Gen", "Given Name", "Middle", "Surname", "Maiden Name", "Birth Year", "Death Year", "Confidence"])

            data = []
            for p in people:
                data.append({
                    "ID": p.id,
                    "Gen": p.generation or "",
                    "Given Name": p.given_name or "",
                    "Middle": p.middle_name or "",
                    "Surname": p.surname or "",
                    "Maiden Name": p.maiden_name or "",
                    "Birth Year": p.birth_year or "",
                    "Death Year": p.death_year or "",
                    "Confidence": p.confidence.value if p.confidence else ""
                })

            return pd.DataFrame(data)

    def get_relationships_df(self) -> pd.DataFrame:
        """Get all relationships as a DataFrame."""
        with self.store.get_session() as session:
            rels = session.query(RelationshipDB).all()

            if not rels:
                return pd.DataFrame(columns=["ID", "Parent ID", "Parent", "Child ID", "Child", "Type", "Confidence"])

            data = []
            for r in rels:
                parent = session.query(PersonDB).filter(PersonDB.id == r.parent_id).first()
                child = session.query(PersonDB).filter(PersonDB.id == r.child_id).first()

                parent_name = f"{parent.given_name} {parent.surname}" if parent else "Unknown"
                child_name = f"{child.given_name} {child.surname}" if child else "Unknown"

                data.append({
                    "ID": r.id,
                    "Parent ID": r.parent_id,
                    "Parent": parent_name,
                    "Child ID": r.child_id,
                    "Child": child_name,
                    "Type": r.relationship_type,
                    "Confidence": r.confidence.value if r.confidence else ""
                })

            return pd.DataFrame(data)

    def get_partnerships_df(self) -> pd.DataFrame:
        """Get all partnerships as a DataFrame."""
        with self.store.get_session() as session:
            parts = session.query(PartnershipDB).all()

            if not parts:
                return pd.DataFrame(columns=["ID", "Person 1 ID", "Person 1", "Person 2 ID", "Person 2", "Type", "Start Year", "End Year", "Sequence", "Confidence"])

            data = []
            for p in parts:
                person1 = session.query(PersonDB).filter(PersonDB.id == p.person1_id).first()
                person2 = session.query(PersonDB).filter(PersonDB.id == p.person2_id).first()

                person1_name = f"{person1.given_name} {person1.surname}" if person1 else "Unknown"
                person2_name = f"{person2.given_name} {person2.surname}" if person2 else "Unknown"

                data.append({
                    "ID": p.id,
                    "Person 1 ID": p.person1_id,
                    "Person 1": person1_name,
                    "Person 2 ID": p.person2_id,
                    "Person 2": person2_name,
                    "Type": p.partnership_type,
                    "Start Year": p.start_year or "",
                    "End Year": p.end_year or "",
                    "Sequence": p.sequence_number or "",
                    "Confidence": p.confidence.value if p.confidence else ""
                })

            return pd.DataFrame(data)

    def add_person(
        self,
        given_name: str,
        surname: str,
        middle_name: str = "",
        maiden_name: str = "",
        birth_year: str = "",
        death_year: str = "",
        generation: str = "",
        confidence: str = "likely"
    ) -> Tuple[str, pd.DataFrame]:
        """Add a new person to the database."""
        try:
            # Validate required fields
            if not given_name or not surname:
                return "Error: Given name and surname are required.", self.get_all_people_df()

            # Convert years to int if provided
            birth_yr = int(birth_year) if birth_year else None
            death_yr = int(death_year) if death_year else None
            gen = int(generation) if generation else None

            # Note: We allow duplicate names since it's common to reuse names across generations
            person_id = self.store.add_person(
                given_name,
                surname,
                middle_name=middle_name if middle_name else None,
                maiden_name=maiden_name if maiden_name else None,
                birth_year=birth_yr,
                death_year=death_yr,
                generation=gen,
                confidence=ConfidenceLevel(confidence)
            )

            return f"Successfully added {given_name} {surname} with ID {person_id}", self.get_all_people_df()

        except Exception as e:
            return f"Error adding person: {str(e)}", self.get_all_people_df()

    def add_relationship(
        self,
        parent_id: str,
        child_id: str,
        rel_type: str = "biological",
        confidence: str = "likely"
    ) -> Tuple[str, pd.DataFrame]:
        """Add a parent-child relationship."""
        try:
            parent_id_int = int(parent_id)
            child_id_int = int(child_id)

            # Check if relationship already exists
            if self.store.has_relationship(parent_id_int, child_id_int, rel_type):
                return f"Relationship already exists.", self.get_relationships_df()

            rel_id = self.store.add_relationship(
                parent_id_int,
                child_id_int,
                rel_type,
                ConfidenceLevel(confidence)
            )

            return f"Successfully added relationship with ID {rel_id}", self.get_relationships_df()

        except ValueError:
            return "Error: Parent ID and Child ID must be numbers.", self.get_relationships_df()
        except Exception as e:
            return f"Error adding relationship: {str(e)}", self.get_relationships_df()

    def add_partnership(
        self,
        person1_id: str,
        person2_id: str,
        partnership_type: str = "marriage",
        start_year: str = "",
        end_year: str = "",
        sequence: str = "",
        confidence: str = "likely"
    ) -> Tuple[str, pd.DataFrame]:
        """Add a partnership/marriage."""
        try:
            p1_id = int(person1_id)
            p2_id = int(person2_id)

            # Check if partnership already exists
            if self.store.has_partnership(p1_id, p2_id):
                return f"Partnership already exists.", self.get_partnerships_df()

            start_yr = int(start_year) if start_year else None
            end_yr = int(end_year) if end_year else None
            seq = int(sequence) if sequence else None

            part_id = self.store.add_partnership(
                p1_id,
                p2_id,
                partnership_type,
                start_year=start_yr,
                end_year=end_yr,
                sequence_number=seq,
                confidence=ConfidenceLevel(confidence)
            )

            return f"Successfully added partnership with ID {part_id}", self.get_partnerships_df()

        except ValueError:
            return "Error: Person IDs must be numbers.", self.get_partnerships_df()
        except Exception as e:
            return f"Error adding partnership: {str(e)}", self.get_partnerships_df()

    def find_keenum_ancestor_path(self, person_id: int) -> Optional[list]:
        """Find the path from a person to their earliest Keenum ancestor.

        Returns a list of (person_id, person_name, generation) tuples from ancestor to descendant.
        """
        with self.store.get_session() as session:
            def get_parents(pid):
                """Get all parents of a person."""
                parent_rels = session.query(RelationshipDB).filter(RelationshipDB.child_id == pid).all()
                parents = []
                for rel in parent_rels:
                    parent = session.query(PersonDB).filter(PersonDB.id == rel.parent_id).first()
                    if parent:
                        parents.append(parent)
                return parents

            def find_path_to_root(pid, visited=None):
                """Recursively find all paths to root ancestors."""
                if visited is None:
                    visited = set()

                if pid in visited:
                    return []

                visited.add(pid)
                person = session.query(PersonDB).filter(PersonDB.id == pid).first()
                if not person:
                    return []

                parents = get_parents(pid)

                # If no parents, this is a root ancestor
                if not parents:
                    return [[person]]

                # Recursively find paths through each parent
                all_paths = []
                for parent in parents:
                    parent_paths = find_path_to_root(parent.id, visited.copy())
                    for path in parent_paths:
                        all_paths.append(path + [person])

                return all_paths

            # Find all paths to root ancestors
            all_paths = find_path_to_root(person_id)

            # Filter for paths that lead to Keenum ancestors
            keenum_paths = []
            for path in all_paths:
                # Check if the root (first person in path) is a Keenum
                if path and path[0].surname and 'keenum' in path[0].surname.lower():
                    keenum_paths.append(path)

            if not keenum_paths:
                return None

            # Find the earliest Keenum ancestor (by generation, then by birth year)
            earliest_path = None
            earliest_gen = float('inf')
            earliest_birth = float('inf')

            for path in keenum_paths:
                root = path[0]
                gen = root.generation if root.generation else float('inf')
                birth = root.birth_year if root.birth_year else float('inf')

                if gen < earliest_gen or (gen == earliest_gen and birth < earliest_birth):
                    earliest_gen = gen
                    earliest_birth = birth
                    earliest_path = path

            if earliest_path:
                # Convert to tuple format (id, name, generation)
                return [(p.id, f"{p.given_name} {p.surname}", p.generation or 0, p.birth_year, p.death_year)
                        for p in earliest_path]

            return None

    def update_person(
        self,
        person_id: str,
        given_name: str,
        surname: str,
        middle_name: str = "",
        maiden_name: str = "",
        birth_year: str = "",
        death_year: str = "",
        generation: str = "",
        confidence: str = "likely"
    ) -> Tuple[str, dict]:
        """Update an existing person's information.

        Returns: (status_message, updated_person_data_dict)
        """
        try:
            pid = int(person_id)

            # Validate person exists
            person = self.store.get_person_by_id(pid)
            if not person:
                return f"Error: Person with ID {pid} not found.", {}

            # Validate required fields
            if not given_name or not surname:
                return "Error: Given name and surname are required.", {}

            # Convert years and generation to int if provided
            birth_yr = int(birth_year) if birth_year.strip() else None
            death_yr = int(death_year) if death_year.strip() else None
            gen = int(generation) if generation.strip() else None

            # Update the person in the database
            with self.store.get_session() as session:
                person_db = session.query(PersonDB).filter(PersonDB.id == pid).first()

                if not person_db:
                    return f"Error: Person with ID {pid} not found in database.", {}

                # Update fields
                person_db.given_name = given_name
                person_db.surname = surname
                person_db.middle_name = middle_name if middle_name.strip() else None
                person_db.maiden_name = maiden_name if maiden_name.strip() else None
                person_db.birth_year = birth_yr
                person_db.death_year = death_yr
                person_db.generation = gen
                person_db.confidence = ConfidenceLevel(confidence)

                session.commit()

                # Return updated person data for display
                updated_data = {
                    "person_id": str(pid),
                    "given_name": person_db.given_name,
                    "middle_name": person_db.middle_name or "",
                    "surname": person_db.surname,
                    "maiden_name": person_db.maiden_name or "",
                    "birth_year": str(person_db.birth_year) if person_db.birth_year else "",
                    "death_year": str(person_db.death_year) if person_db.death_year else "",
                    "generation": str(person_db.generation) if person_db.generation else "",
                    "confidence": person_db.confidence.value
                }

                return f"✅ Successfully updated {given_name} {surname} (ID: {pid})", updated_data

        except ValueError as e:
            return f"Error: Invalid input - {str(e)}", {}
        except Exception as e:
            return f"Error updating person: {str(e)}", {}

    def load_person_for_editing(self, person_id: str) -> Tuple[str, str, str, str, str, str, str, str, str]:
        """Load a person's data for editing.

        Returns tuple of: (status, person_id, given_name, middle_name, surname, maiden_name,
                          birth_year, death_year, generation, confidence)
        """
        try:
            if not person_id.strip():
                return ("Enter a Person ID to load", "", "", "", "", "", "", "", "", "likely")

            pid = int(person_id)
            person = self.store.get_person_by_id(pid)

            if not person:
                return (f"❌ Person with ID {pid} not found.", "", "", "", "", "", "", "", "", "likely")

            return (
                f"✅ Loaded: {person.given_name} {person.surname}",
                str(pid),
                person.given_name or "",
                person.middle_name or "",
                person.surname or "",
                person.maiden_name or "",
                str(person.birth_year) if person.birth_year else "",
                str(person.death_year) if person.death_year else "",
                str(person.generation) if person.generation else "",
                person.confidence.value if person.confidence else "likely"
            )

        except ValueError:
            return ("Error: Person ID must be a number.", "", "", "", "", "", "", "", "", "likely")
        except Exception as e:
            return (f"Error loading person: {str(e)}", "", "", "", "", "", "", "", "", "likely")

    def get_person_details(self, person_id: str) -> str:
        """Get detailed information about a person including relationships."""
        try:
            pid = int(person_id)
            person = self.store.get_person_by_id(pid)

            if not person:
                return f"Person with ID {pid} not found."

            # Build details string
            details = f"**{person.given_name}"
            if person.middle_name:
                details += f" {person.middle_name}"
            details += f" {person.surname}**\n\n"

            if person.maiden_name:
                details += f"*Maiden name: {person.maiden_name}*\n"

            if person.birth_year:
                details += f"Born: {person.birth_year}\n"
            if person.death_year:
                details += f"Died: {person.death_year}\n"

            if person.generation:
                details += f"Generation: {person.generation}\n"

            details += f"Confidence: {person.confidence.value}\n"

            # Find and display lineage to earliest Keenum ancestor
            lineage_path = self.find_keenum_ancestor_path(pid)
            if lineage_path and len(lineage_path) > 1:
                details += "\n---\n"
                details += "\n**Lineage to Earliest Keenum Ancestor:**\n\n"

                # Display the path from ancestor to this person
                for i, (p_id, p_name, p_gen, p_birth, p_death) in enumerate(lineage_path):
                    indent = "  " * i
                    arrow = "└→ " if i > 0 else ""

                    # Build the person line with dates
                    dates = ""
                    if p_birth or p_death:
                        dates = f" ({p_birth or '?'}-{p_death or '?'})"

                    # Highlight if this is the current person
                    if p_id == pid:
                        details += f"{indent}{arrow}**{p_name}**{dates} ← *You are here* (Gen {p_gen})\n"
                    elif i == 0:
                        details += f"{indent}{arrow}{p_name}{dates} - *Earliest Keenum Ancestor* (Gen {p_gen})\n"
                    else:
                        details += f"{indent}{arrow}{p_name}{dates} (Gen {p_gen})\n"

                # Calculate relationship description
                generations_from_ancestor = len(lineage_path) - 1
                if generations_from_ancestor == 1:
                    relationship = "child"
                elif generations_from_ancestor == 2:
                    relationship = "grandchild"
                elif generations_from_ancestor == 3:
                    relationship = "great-grandchild"
                elif generations_from_ancestor > 3:
                    greats = "great-" * (generations_from_ancestor - 2)
                    relationship = f"{greats}grandchild"
                else:
                    relationship = "self"

                ancestor_name = lineage_path[0][1]
                details += f"\n*This person is the **{relationship}** of {ancestor_name}*\n"

            elif person.surname and 'keenum' in person.surname.lower() and lineage_path and len(lineage_path) == 1:
                details += "\n---\n"
                details += "\n**Note:** This person appears to be a root Keenum ancestor with no recorded parents.\n"

            # Get relationships
            details += "\n---\n"
            details += "\n**Direct Family Relationships:**\n"

            with self.store.get_session() as session:
                # Parents
                parent_rels = session.query(RelationshipDB).filter(RelationshipDB.child_id == pid).all()
                if parent_rels:
                    details += "\n**Parents:**\n"
                    for rel in parent_rels:
                        parent = session.query(PersonDB).filter(PersonDB.id == rel.parent_id).first()
                        if parent:
                            birth_death = ""
                            if parent.birth_year or parent.death_year:
                                birth_death = f" ({parent.birth_year or '?'}-{parent.death_year or '?'})"
                            details += f"- {parent.given_name} {parent.surname}{birth_death} (ID: {parent.id}, {rel.relationship_type})\n"

                # Siblings (people who share at least one parent)
                if parent_rels:
                    siblings_set = set()
                    for parent_rel in parent_rels:
                        sibling_rels = session.query(RelationshipDB).filter(
                            RelationshipDB.parent_id == parent_rel.parent_id,
                            RelationshipDB.child_id != pid
                        ).all()
                        for sib_rel in sibling_rels:
                            siblings_set.add(sib_rel.child_id)

                    if siblings_set:
                        details += "\n**Siblings:**\n"
                        for sib_id in sorted(siblings_set):
                            sibling = session.query(PersonDB).filter(PersonDB.id == sib_id).first()
                            if sibling:
                                birth_death = ""
                                if sibling.birth_year or sibling.death_year:
                                    birth_death = f" ({sibling.birth_year or '?'}-{sibling.death_year or '?'})"
                                details += f"- {sibling.given_name} {sibling.surname}{birth_death} (ID: {sibling.id})\n"

                # Partnerships/Spouses
                partnerships = session.query(PartnershipDB).filter(
                    (PartnershipDB.person1_id == pid) | (PartnershipDB.person2_id == pid)
                ).all()

                if partnerships:
                    details += "\n**Spouses/Partners:**\n"
                    for part in partnerships:
                        other_id = part.person2_id if part.person1_id == pid else part.person1_id
                        other = session.query(PersonDB).filter(PersonDB.id == other_id).first()
                        if other:
                            birth_death = ""
                            if other.birth_year or other.death_year:
                                birth_death = f" ({other.birth_year or '?'}-{other.death_year or '?'})"
                            partner_info = f"- {other.given_name} {other.surname}{birth_death} (ID: {other.id}, {part.partnership_type})"
                            if part.start_year:
                                partner_info += f" - married {part.start_year}"
                            if part.end_year:
                                partner_info += f" to {part.end_year}"
                            if part.sequence_number:
                                partner_info += f" (marriage #{part.sequence_number})"
                            details += partner_info + "\n"

                # Children
                child_rels = session.query(RelationshipDB).filter(RelationshipDB.parent_id == pid).all()
                if child_rels:
                    details += "\n**Children:**\n"
                    for rel in child_rels:
                        child = session.query(PersonDB).filter(PersonDB.id == rel.child_id).first()
                        if child:
                            birth_death = ""
                            if child.birth_year or child.death_year:
                                birth_death = f" ({child.birth_year or '?'}-{child.death_year or '?'})"
                            details += f"- {child.given_name} {child.surname}{birth_death} (ID: {child.id}, {rel.relationship_type})\n"

            return details

        except ValueError:
            return "Error: Person ID must be a number."
        except Exception as e:
            return f"Error getting person details: {str(e)}"

    def create_interface(self):
        """Create the Gradio interface."""
        with gr.Blocks(title="Genealogy Data Entry Tool") as demo:
            gr.Markdown("# Genealogy Data Entry & Verification Tool")
            gr.Markdown("Tool for entering and verifying genealogical data for the Carpenter/Keenum family.")

            with gr.Tabs():
                # Tab 1: View All People
                with gr.Tab("View People"):
                    gr.Markdown("## All People in Database")
                    gr.Markdown("*Click on any row to view detailed information about that person*")

                    # Search filters
                    with gr.Row():
                        search_given_name = gr.Textbox(
                            label="Search by Given Name",
                            placeholder="e.g., John, Mary",
                            scale=2
                        )
                        search_surname = gr.Textbox(
                            label="Search by Surname",
                            placeholder="e.g., Keenum, Smith",
                            scale=2
                        )
                        search_btn = gr.Button("Search", variant="primary", scale=1)
                        clear_btn = gr.Button("Clear", scale=1)

                    people_table = gr.Dataframe(
                        value=self.get_all_people_df(),
                        interactive=False
                    )

                    # Person details panel (appears when clicking a row)
                    gr.Markdown("### Person Details")
                    gr.Markdown("*Select a person from the table above to see their details*")
                    selected_person_details = gr.Markdown(value="", label="Details")

                    # Search functionality
                    search_btn.click(
                        fn=self.get_all_people_df,
                        inputs=[search_given_name, search_surname],
                        outputs=people_table
                    )

                    # Allow search on Enter key in either field
                    search_given_name.submit(
                        fn=self.get_all_people_df,
                        inputs=[search_given_name, search_surname],
                        outputs=people_table
                    )

                    search_surname.submit(
                        fn=self.get_all_people_df,
                        inputs=[search_given_name, search_surname],
                        outputs=people_table
                    )

                    # Clear filters
                    clear_btn.click(
                        fn=lambda: (self.get_all_people_df(), "", ""),
                        outputs=[people_table, search_given_name, search_surname]
                    )

                    # When a row is selected, show person details
                    def show_details_from_table(table_data, evt: gr.SelectData):
                        """Extract person ID from selected row and show details."""
                        try:
                            # evt.index is (row, column)
                            row_idx = evt.index[0]

                            # Convert table data to DataFrame if it isn't already
                            if isinstance(table_data, pd.DataFrame):
                                df = table_data
                            else:
                                df = pd.DataFrame(table_data)

                            # Get the ID from the first column of the selected row
                            if not df.empty and row_idx < len(df):
                                person_id = str(df.iloc[row_idx]['ID'])
                                return self.get_person_details(person_id)

                            return "Could not retrieve person details."
                        except Exception as e:
                            return f"Error: {str(e)}"

                    people_table.select(
                        fn=show_details_from_table,
                        inputs=[people_table],
                        outputs=selected_person_details
                    )

                # Tab 2: Add Person
                with gr.Tab("Add Person"):
                    gr.Markdown("## Add New Person")
                    with gr.Row():
                        given_name_input = gr.Textbox(label="Given Name *", placeholder="John")
                        middle_name_input = gr.Textbox(label="Middle Name", placeholder="William")
                        surname_input = gr.Textbox(label="Surname *", placeholder="Keenum")

                    with gr.Row():
                        maiden_name_input = gr.Textbox(label="Maiden Name", placeholder="Smith")
                        generation_input = gr.Textbox(label="Generation #", placeholder="1")
                        birth_year_input = gr.Textbox(label="Birth Year", placeholder="1850")
                        death_year_input = gr.Textbox(label="Death Year", placeholder="1920")

                    confidence_input = gr.Dropdown(
                        choices=["confirmed", "likely", "possible", "uncertain"],
                        value="likely",
                        label="Confidence Level"
                    )

                    add_person_btn = gr.Button("Add Person", variant="primary")
                    add_person_status = gr.Textbox(label="Status", interactive=False)
                    add_person_table = gr.Dataframe(label="Updated People List")

                    add_person_btn.click(
                        fn=self.add_person,
                        inputs=[given_name_input, surname_input, middle_name_input, maiden_name_input,
                                birth_year_input, death_year_input, generation_input, confidence_input],
                        outputs=[add_person_status, add_person_table]
                    )

                # Tab 3: Edit Person
                with gr.Tab("Edit Person"):
                    gr.Markdown("## Edit Existing Person")
                    gr.Markdown("*Enter a Person ID and click Load to edit that person's information*")
                    gr.Markdown("*Use the View People tab to find Person IDs*")

                    # Lookup section
                    with gr.Row():
                        edit_person_id_lookup = gr.Textbox(
                            label="Person ID to Edit",
                            placeholder="Enter ID (e.g., 1)",
                            scale=3
                        )
                        load_person_btn = gr.Button("Load Person", variant="secondary", scale=1)

                    edit_load_status = gr.Textbox(label="Load Status", interactive=False)

                    # Editable fields
                    gr.Markdown("### Person Information")
                    edit_person_id_hidden = gr.Textbox(label="Person ID", interactive=False, visible=True)

                    with gr.Row():
                        edit_given_name = gr.Textbox(label="Given Name *", placeholder="John")
                        edit_middle_name = gr.Textbox(label="Middle Name", placeholder="William")
                        edit_surname = gr.Textbox(label="Surname *", placeholder="Keenum")

                    with gr.Row():
                        edit_maiden_name = gr.Textbox(label="Maiden Name", placeholder="Smith")
                        edit_generation = gr.Textbox(label="Generation #", placeholder="1")
                        edit_birth_year = gr.Textbox(label="Birth Year", placeholder="1850")
                        edit_death_year = gr.Textbox(label="Death Year", placeholder="1920")

                    edit_confidence = gr.Dropdown(
                        choices=["confirmed", "likely", "possible", "uncertain"],
                        value="likely",
                        label="Confidence Level"
                    )

                    # Save button
                    with gr.Row():
                        save_person_btn = gr.Button("Save Changes", variant="primary", scale=1)
                        cancel_edit_btn = gr.Button("Clear Form", scale=1)

                    edit_save_status = gr.Textbox(label="Save Status", interactive=False)
                    edit_person_table = gr.Dataframe(label="Updated People List")

                    # Load person button handler
                    def handle_load_person(person_id):
                        """Load person and return updated form fields."""
                        result = self.load_person_for_editing(person_id)
                        # Returns: (status, person_id, given_name, middle_name, surname, maiden_name,
                        #           birth_year, death_year, generation, confidence)
                        return result  # This returns the tuple directly to all outputs

                    load_person_btn.click(
                        fn=handle_load_person,
                        inputs=edit_person_id_lookup,
                        outputs=[
                            edit_load_status,
                            edit_person_id_hidden,
                            edit_given_name,
                            edit_middle_name,
                            edit_surname,
                            edit_maiden_name,
                            edit_birth_year,
                            edit_death_year,
                            edit_generation,
                            edit_confidence
                        ]
                    )

                    # Save person button handler
                    def handle_save_person(person_id, given_name, surname, middle_name, maiden_name,
                                          birth_year, death_year, generation, confidence):
                        """Save updated person and return status."""
                        if not person_id:
                            return "Error: Please load a person first.", self.get_all_people_df()

                        status, updated_data = self.update_person(
                            person_id, given_name, surname, middle_name, maiden_name,
                            birth_year, death_year, generation, confidence
                        )
                        return status, self.get_all_people_df()

                    save_person_btn.click(
                        fn=handle_save_person,
                        inputs=[
                            edit_person_id_hidden,
                            edit_given_name,
                            edit_surname,
                            edit_middle_name,
                            edit_maiden_name,
                            edit_birth_year,
                            edit_death_year,
                            edit_generation,
                            edit_confidence
                        ],
                        outputs=[edit_save_status, edit_person_table]
                    )

                    # Clear form button handler
                    def clear_edit_form():
                        """Clear all edit form fields."""
                        return (
                            "",  # load status
                            "",  # person_id
                            "",  # given_name
                            "",  # middle_name
                            "",  # surname
                            "",  # maiden_name
                            "",  # birth_year
                            "",  # death_year
                            "",  # generation
                            "likely",  # confidence
                            "",  # save status
                            self.get_all_people_df()  # table
                        )

                    cancel_edit_btn.click(
                        fn=clear_edit_form,
                        outputs=[
                            edit_load_status,
                            edit_person_id_hidden,
                            edit_given_name,
                            edit_middle_name,
                            edit_surname,
                            edit_maiden_name,
                            edit_birth_year,
                            edit_death_year,
                            edit_generation,
                            edit_confidence,
                            edit_save_status,
                            edit_person_table
                        ]
                    )

                # Tab 4: Add Relationship
                with gr.Tab("Add Relationship"):
                    gr.Markdown("## Add Parent-Child Relationship")
                    gr.Markdown("*Use the View People tab to find Person IDs*")

                    with gr.Row():
                        parent_id_input = gr.Textbox(label="Parent ID *", placeholder="1")
                        child_id_input = gr.Textbox(label="Child ID *", placeholder="2")

                    with gr.Row():
                        rel_type_input = gr.Dropdown(
                            choices=["biological", "adoptive", "step"],
                            value="biological",
                            label="Relationship Type"
                        )
                        rel_confidence_input = gr.Dropdown(
                            choices=["confirmed", "likely", "possible", "uncertain"],
                            value="likely",
                            label="Confidence Level"
                        )

                    add_rel_btn = gr.Button("Add Relationship", variant="primary")
                    add_rel_status = gr.Textbox(label="Status", interactive=False)
                    add_rel_table = gr.Dataframe(label="Updated Relationships")

                    add_rel_btn.click(
                        fn=self.add_relationship,
                        inputs=[parent_id_input, child_id_input, rel_type_input, rel_confidence_input],
                        outputs=[add_rel_status, add_rel_table]
                    )

                # Tab 5: Add Partnership
                with gr.Tab("Add Partnership"):
                    gr.Markdown("## Add Marriage/Partnership")
                    gr.Markdown("*Use the View People tab to find Person IDs*")

                    with gr.Row():
                        person1_id_input = gr.Textbox(label="Person 1 ID *", placeholder="1")
                        person2_id_input = gr.Textbox(label="Person 2 ID *", placeholder="2")

                    with gr.Row():
                        part_type_input = gr.Dropdown(
                            choices=["marriage", "partnership"],
                            value="marriage",
                            label="Partnership Type"
                        )
                        start_year_input = gr.Textbox(label="Start Year", placeholder="1870")
                        end_year_input = gr.Textbox(label="End Year (optional)", placeholder="1920")

                    with gr.Row():
                        sequence_input = gr.Textbox(label="Sequence # (1st, 2nd marriage)", placeholder="1")
                        part_confidence_input = gr.Dropdown(
                            choices=["confirmed", "likely", "possible", "uncertain"],
                            value="likely",
                            label="Confidence Level"
                        )

                    add_part_btn = gr.Button("Add Partnership", variant="primary")
                    add_part_status = gr.Textbox(label="Status", interactive=False)
                    add_part_table = gr.Dataframe(label="Updated Partnerships")

                    add_part_btn.click(
                        fn=self.add_partnership,
                        inputs=[person1_id_input, person2_id_input, part_type_input,
                                start_year_input, end_year_input, sequence_input, part_confidence_input],
                        outputs=[add_part_status, add_part_table]
                    )

                # Tab 6: View Relationships
                with gr.Tab("View Relationships"):
                    gr.Markdown("## All Relationships")
                    rel_refresh = gr.Button("Refresh")
                    rel_table = gr.Dataframe(
                        value=self.get_relationships_df(),
                        interactive=False
                    )
                    rel_refresh.click(
                        fn=self.get_relationships_df,
                        outputs=rel_table
                    )

                # Tab 7: View Partnerships
                with gr.Tab("View Partnerships"):
                    gr.Markdown("## All Partnerships")
                    part_refresh = gr.Button("Refresh")
                    part_table = gr.Dataframe(
                        value=self.get_partnerships_df(),
                        interactive=False
                    )
                    part_refresh.click(
                        fn=self.get_partnerships_df,
                        outputs=part_table
                    )

                # Tab 8: Person Details
                with gr.Tab("Person Details"):
                    gr.Markdown("## View Person Details")
                    person_id_lookup = gr.Textbox(label="Person ID", placeholder="1")
                    lookup_btn = gr.Button("Lookup")
                    person_details_output = gr.Markdown()

                    lookup_btn.click(
                        fn=self.get_person_details,
                        inputs=person_id_lookup,
                        outputs=person_details_output
                    )

        return demo


def main():
    """Run the data entry tool."""
    tool = GenealogyDataEntry()
    demo = tool.create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7861, share=False)


if __name__ == "__main__":
    main()
