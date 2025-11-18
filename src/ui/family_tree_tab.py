"""Family tree visualization tab for Gradio UI."""

import gradio as gr
from typing import Optional, List, Tuple

from ..visualizations.graph_builder import FamilyGraphBuilder
from ..visualizations.d3_tidy_tree import D3TidyTreeVisualizer
from ..utils.config import Settings


class FamilyTreeTab:
    """Manages family tree visualization UI."""

    def __init__(self, settings: Settings):
        """Initialize family tree tab.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.graph_builder = FamilyGraphBuilder(settings)
        self.visualizer = D3TidyTreeVisualizer()

    def search_people(self, search_term: str) -> gr.Dropdown:
        """Search for people and update dropdown choices.

        Args:
            search_term: Search term

        Returns:
            Updated dropdown
        """
        if not search_term or len(search_term) < 2:
            return gr.Dropdown(choices=[], value=None)

        results = self.graph_builder.search_people(search_term)

        # Format choices as (display_name, person_id)
        choices = [(r["name"], r["id"]) for r in results]

        return gr.Dropdown(
            choices=choices,
            value=choices[0][1] if choices else None,
            label="Select Person",
        )

    def get_all_surnames(self) -> List[str]:
        """Get all surnames for filter dropdown.

        Returns:
            List of surnames
        """
        surnames = self.graph_builder.get_all_surnames()
        return ["All"] + surnames

    def generate_tree(
        self,
        root_person_id: Optional[int],
        max_generations: Optional[int],
        include_ancestors: bool,
        include_descendants: bool,
        surname_filter: Optional[str],
        color_by_surname: bool,
        highlight_person_id: Optional[int],
    ) -> Tuple[str, str]:
        """Generate family tree visualization.

        Args:
            root_person_id: Root person ID
            max_generations: Max generations to show
            include_ancestors: Include ancestors
            include_descendants: Include descendants
            surname_filter: Surname to filter by
            color_by_surname: Whether to color by surname
            highlight_person_id: Person ID to highlight

        Returns:
            Tuple of (HTML string, status message)
        """
        try:
            # Enforce node limit to prevent performance issues
            MAX_NODES = 200

            # Build graph
            if surname_filter == "All" or not surname_filter:
                surname_filter = None

            G = self.graph_builder.build_graph(
                root_person_id=root_person_id,
                max_generations=max_generations if max_generations and max_generations > 0 else None,
                include_ancestors=include_ancestors,
                include_descendants=include_descendants,
                surname_filter=surname_filter,
            )

            if len(G.nodes) == 0:
                empty_html = self.visualizer._create_empty_html(
                    "No people found matching the criteria"
                )
                return empty_html, "No people found matching the criteria"

            # Check node limit
            if len(G.nodes) > MAX_NODES:
                empty_html = self.visualizer._create_empty_html(
                    f"Too many nodes to display ({len(G.nodes)}). Please narrow your search.<br/>"
                    f"Maximum: {MAX_NODES} nodes.<br/>"
                    f"Try: selecting a specific person, reducing generations, or filtering by surname."
                )
                return empty_html, f"Too many nodes ({len(G.nodes)}). Max is {MAX_NODES}. Please narrow your search."

            # Generate title
            title = "Family Tree"
            if root_person_id and root_person_id in G.nodes:
                root_name = G.nodes[root_person_id]["full_name"]
                title = f"Family Tree - {root_name}"

            # Create visualization
            html = self.visualizer.visualize(
                G,
                root_person_id=root_person_id,
                highlight_person_id=highlight_person_id,
                color_by_surname=color_by_surname,
                title=title,
            )

            status = f"Showing {len(G.nodes)} people and {len(G.edges)} relationships"
            return html, status

        except Exception as e:
            empty_html = self.visualizer._create_empty_html(f"Error: {str(e)}")
            return empty_html, f"Error generating tree: {str(e)}"

    def export_html(
        self,
        html: str,
        filename: str = "family_tree.html",
    ) -> str:
        """Export visualization to HTML file.

        Args:
            html: HTML string
            filename: Output filename

        Returns:
            Status message
        """
        try:
            filepath = f"data/exports/{filename}"
            self.visualizer.export_to_html(html, filepath)
            return f"Exported to {filepath}"
        except Exception as e:
            return f"Error exporting: {str(e)}"


def create_family_tree_tab(settings: Settings) -> gr.Tab:
    """Create family tree visualization tab.

    Args:
        settings: Application settings

    Returns:
        Gradio Tab
    """
    tab_instance = FamilyTreeTab(settings)

    with gr.Tab("Family Tree") as tab:
        gr.Markdown("""
        ## Interactive Family Tree Visualization

        Visualize family relationships in a dbt lineage-style diagram.
        Use the filters below to customize the view.
        """)

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Filters & Controls")

                # Person search
                search_box = gr.Textbox(
                    label="Search for Person",
                    placeholder="Enter name to search...",
                    info="Search by first or last name",
                )

                person_dropdown = gr.Dropdown(
                    label="Select Root Person",
                    choices=[],
                    value=None,
                    info="Select a person to center the tree on (leave empty for all people)",
                )

                # Generation controls
                max_generations = gr.Slider(
                    label="Max Generations",
                    minimum=1,
                    maximum=10,
                    value=2,
                    step=1,
                    info="Maximum number of generations to display (2-3 recommended)",
                )

                with gr.Row():
                    include_ancestors = gr.Checkbox(
                        label="Include Ancestors",
                        value=True,
                    )
                    include_descendants = gr.Checkbox(
                        label="Include Descendants",
                        value=True,
                    )

                # Surname filter
                surname_filter = gr.Dropdown(
                    label="Filter by Surname",
                    choices=tab_instance.get_all_surnames(),
                    value="All",
                    info="Show only people with this surname",
                )

                # Display options
                color_by_surname = gr.Checkbox(
                    label="Color by Surname",
                    value=True,
                    info="Color nodes by surname for easy identification",
                )

                highlight_search = gr.Textbox(
                    label="Highlight Person",
                    placeholder="Search to highlight...",
                    info="Search for a person to highlight in purple",
                )

                highlight_dropdown = gr.Dropdown(
                    label="Select Person to Highlight",
                    choices=[],
                    value=None,
                )

                # Generate button
                generate_btn = gr.Button(
                    "Generate Tree",
                    variant="primary",
                    size="lg",
                )

            with gr.Column(scale=3):
                # Visualization output
                status_text = gr.Textbox(
                    label="Status",
                    value="Click 'Generate Tree' to create visualization",
                    interactive=False,
                )

                plot_output = gr.HTML(
                    label="Family Tree Visualization",
                    value="<div style='padding: 40px; text-align: center; color: #64748B;'>Click 'Generate Tree' to create visualization</div>",
                )

                # Export controls
                with gr.Row():
                    export_filename = gr.Textbox(
                        label="Export Filename",
                        value="family_tree.html",
                        scale=3,
                    )
                    export_btn = gr.Button(
                        "Export HTML",
                        scale=1,
                    )

                export_status = gr.Textbox(
                    label="Export Status",
                    interactive=False,
                )

        # Event handlers

        # Search for root person
        search_box.change(
            tab_instance.search_people,
            inputs=[search_box],
            outputs=[person_dropdown],
        )

        # Search for highlight person
        highlight_search.change(
            tab_instance.search_people,
            inputs=[highlight_search],
            outputs=[highlight_dropdown],
        )

        # Generate tree
        generate_btn.click(
            tab_instance.generate_tree,
            inputs=[
                person_dropdown,
                max_generations,
                include_ancestors,
                include_descendants,
                surname_filter,
                color_by_surname,
                highlight_dropdown,
            ],
            outputs=[plot_output, status_text],
        )

        # Export HTML
        export_btn.click(
            tab_instance.export_html,
            inputs=[plot_output, export_filename],
            outputs=[export_status],
        )

    return tab
