"""Family tree visualization using Plotly."""

from typing import Dict, List, Tuple, Optional, Set
import networkx as nx
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import colorsys


class FamilyTreeVisualizer:
    """Visualizes family tree using Plotly with dbt-style lineage layout."""

    # Color palette inspired by dbt lineage (teal/blue spectrum)
    DEFAULT_COLOR = "#1F8297"  # Teal
    HIGHLIGHT_COLOR = "#A855F7"  # Purple
    MARRIAGE_LINE_COLOR = "#64748B"  # Slate gray
    PARENT_CHILD_COLOR = "#94A3B8"  # Light slate

    def __init__(self):
        """Initialize visualizer."""
        self.node_width = 180
        self.node_height = 60
        self.horizontal_spacing = 300
        self.vertical_spacing = 120

    def visualize(
        self,
        G: nx.DiGraph,
        highlight_person_id: Optional[int] = None,
        color_by_surname: bool = True,
        title: str = "Family Tree",
    ) -> Figure:
        """Create interactive family tree visualization.

        Args:
            G: NetworkX directed graph from FamilyGraphBuilder
            highlight_person_id: Person ID to highlight
            color_by_surname: Color nodes by surname
            title: Chart title

        Returns:
            Plotly Figure object
        """
        if len(G.nodes) == 0:
            return self._create_empty_figure("No data to display")

        # Calculate hierarchical layout (left to right)
        pos = self._calculate_layout(G)

        # Generate color mapping
        if color_by_surname:
            color_map = self._generate_surname_colors(G)
        else:
            color_map = {node: self.DEFAULT_COLOR for node in G.nodes}

        # Override with highlight color if specified
        if highlight_person_id and highlight_person_id in G.nodes:
            color_map[highlight_person_id] = self.HIGHLIGHT_COLOR

        # Create figure
        fig = go.Figure()

        # Add parent-child edges (arrows)
        self._add_parent_child_edges(fig, G, pos)

        # Add marriage/partnership connections
        self._add_marriage_connections(fig, G, pos)

        # Add person nodes
        self._add_person_nodes(fig, G, pos, color_map)

        # Configure layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=20, color="#1E293B"),
                x=0.5,
                xanchor="center",
            ),
            showlegend=True,
            hovermode="closest",
            plot_bgcolor="#F8FAFC",
            paper_bgcolor="white",
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                title="",
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                title="",
            ),
            margin=dict(l=20, r=20, t=60, b=20),
            height=800,
        )

        # Add legend for surnames if color coding is enabled
        if color_by_surname:
            self._add_surname_legend(fig, G, color_map)

        return fig

    def _calculate_layout(self, G: nx.DiGraph) -> Dict[int, Tuple[float, float]]:
        """Calculate hierarchical left-to-right layout positions.

        Args:
            G: NetworkX directed graph

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        # Use fast generation-based layout
        # Calculate generation for each node
        generations = self._calculate_generations(G)

        # Group nodes by generation
        gen_groups = {}
        for node, gen in generations.items():
            if gen not in gen_groups:
                gen_groups[gen] = []
            gen_groups[gen].append(node)

        # Assign positions
        pos = {}
        for gen, nodes in gen_groups.items():
            x = gen * self.horizontal_spacing
            # Distribute vertically
            y_start = -(len(nodes) - 1) * self.vertical_spacing / 2
            for i, node in enumerate(sorted(nodes, key=lambda n: G.nodes[n].get("surname", ""))):
                y = y_start + i * self.vertical_spacing
                pos[node] = (x, y)

        return pos

    def _calculate_generations(self, G: nx.DiGraph) -> Dict[int, int]:
        """Calculate generation number for each node.

        Args:
            G: NetworkX directed graph

        Returns:
            Dictionary mapping node IDs to generation numbers
        """
        generations = {}

        # Find root nodes (no parents)
        root_nodes = [n for n in G.nodes if G.in_degree(n) == 0]

        if not root_nodes:
            # If there are cycles or all nodes have parents, use arbitrary starting point
            root_nodes = [list(G.nodes)[0]]

        # BFS to assign generations
        from collections import deque
        queue = deque([(node, 0) for node in root_nodes])
        visited = set()

        while queue:
            node, gen = queue.popleft()
            if node in visited:
                continue
            visited.add(node)

            generations[node] = gen

            # Add children to queue
            for child in G.successors(node):
                if child not in visited:
                    queue.append((child, gen + 1))

        # Handle any unvisited nodes
        for node in G.nodes:
            if node not in generations:
                generations[node] = 0

        return generations

    def _generate_surname_colors(self, G: nx.DiGraph) -> Dict[int, str]:
        """Generate color mapping for surnames.

        Args:
            G: NetworkX directed graph

        Returns:
            Dictionary mapping node IDs to color hex codes
        """
        # Get all unique surnames
        surnames = set()
        for node in G.nodes:
            surname = G.nodes[node].get("surname", "Unknown")
            surnames.add(surname)

        # Generate distinct colors for each surname
        surname_colors = {}
        sorted_surnames = sorted(surnames)

        for i, surname in enumerate(sorted_surnames):
            # Use HSL color space for distinct colors
            hue = i / len(sorted_surnames)
            # Keep saturation and lightness in ranges that look good
            saturation = 0.6
            lightness = 0.5

            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            color = f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
            surname_colors[surname] = color

        # Map nodes to colors based on surname
        color_map = {}
        for node in G.nodes:
            surname = G.nodes[node].get("surname", "Unknown")
            color_map[node] = surname_colors.get(surname, self.DEFAULT_COLOR)

        return color_map

    def _add_parent_child_edges(
        self, fig: Figure, G: nx.DiGraph, pos: Dict[int, Tuple[float, float]]
    ):
        """Add parent-child relationship edges with arrows.

        Args:
            fig: Plotly figure
            G: NetworkX directed graph
            pos: Node positions
        """
        edge_x = []
        edge_y = []

        for parent, child in G.edges():
            if G.edges[parent, child].get("edge_type") == "parent_child":
                x0, y0 = pos[parent]
                x1, y1 = pos[child]

                # Adjust for node dimensions
                x0 += self.node_width / 2
                x1 -= self.node_width / 2

                # Add edge line
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

        if edge_x:
            fig.add_trace(go.Scatter(
                x=edge_x,
                y=edge_y,
                mode="lines",
                line=dict(color=self.PARENT_CHILD_COLOR, width=2),
                hoverinfo="none",
                showlegend=False,
                name="Parent-Child",
            ))

    def _add_arrowheads(
        self, fig: Figure, G: nx.DiGraph, pos: Dict[int, Tuple[float, float]]
    ):
        """Add arrowheads to parent-child edges.

        Args:
            fig: Plotly figure
            G: NetworkX directed graph
            pos: Node positions
        """
        for parent, child in G.edges():
            if G.edges[parent, child].get("edge_type") == "parent_child":
                x0, y0 = pos[parent]
                x1, y1 = pos[child]

                # Arrow position (at the child node)
                x0 += self.node_width / 2
                x1 -= self.node_width / 2

                fig.add_annotation(
                    x=x1,
                    y=y1,
                    ax=x0,
                    ay=y0,
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor=self.PARENT_CHILD_COLOR,
                )

    def _add_marriage_connections(
        self, fig: Figure, G: nx.DiGraph, pos: Dict[int, Tuple[float, float]]
    ):
        """Add marriage/partnership connections as horizontal lines.

        Args:
            fig: Plotly figure
            G: NetworkX directed graph
            pos: Node positions
        """
        marriage_x = []
        marriage_y = []

        # Track which partnerships we've already drawn
        drawn_partnerships = set()

        for node in G.nodes:
            partnerships = G.nodes[node].get("partnerships", [])
            for partnership in partnerships:
                partner_id = partnership["partner_id"]

                # Skip if we've already drawn this partnership
                pair = tuple(sorted([node, partner_id]))
                if pair in drawn_partnerships:
                    continue
                drawn_partnerships.add(pair)

                # Only draw if both nodes are in the graph
                if partner_id in pos:
                    x0, y0 = pos[node]
                    x1, y1 = pos[partner_id]

                    # Draw horizontal-ish line between spouses
                    # Adjust for node dimensions
                    if x0 < x1:
                        x0 += self.node_width / 2
                        x1 -= self.node_width / 2
                    else:
                        x0 -= self.node_width / 2
                        x1 += self.node_width / 2

                    marriage_x.extend([x0, x1, None])
                    marriage_y.extend([y0, y1, None])

        if marriage_x:
            fig.add_trace(go.Scatter(
                x=marriage_x,
                y=marriage_y,
                mode="lines",
                line=dict(color=self.MARRIAGE_LINE_COLOR, width=2, dash="dot"),
                hoverinfo="none",
                showlegend=True,
                name="Marriage/Partnership",
            ))

    def _add_person_nodes(
        self,
        fig: Figure,
        G: nx.DiGraph,
        pos: Dict[int, Tuple[float, float]],
        color_map: Dict[int, str],
    ):
        """Add person nodes as interactive rectangles.

        Args:
            fig: Plotly figure
            G: NetworkX directed graph
            pos: Node positions
            color_map: Node color mapping
        """
        for node in G.nodes:
            x, y = pos[node]
            node_data = G.nodes[node]

            # Build hover text
            hover_text = self._build_hover_text(node_data)

            # Build display label
            label = node_data.get("given_name", "Unknown")
            surname = node_data.get("surname", "")
            if surname:
                label += f" {surname}"
            date_str = node_data.get("date_str", "")
            if date_str:
                label += f"<br>{date_str}"

            # Add rectangle for node
            color = color_map.get(node, self.DEFAULT_COLOR)

            # Add node as a rectangle using shapes
            fig.add_shape(
                type="rect",
                x0=x - self.node_width / 2,
                y0=y - self.node_height / 2,
                x1=x + self.node_width / 2,
                y1=y + self.node_height / 2,
                line=dict(color="#E2E8F0", width=2),
                fillcolor=color,
                opacity=0.9,
            )

            # Add text label
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode="text",
                text=label,
                textposition="middle center",
                textfont=dict(size=11, color="white", family="Arial"),
                hovertext=hover_text,
                hoverinfo="text",
                showlegend=False,
                name=label,
            ))

    def _build_hover_text(self, node_data: Dict) -> str:
        """Build hover text for a person node.

        Args:
            node_data: Node data dictionary

        Returns:
            Formatted hover text
        """
        lines = []

        # Name
        full_name = node_data.get("full_name", "Unknown")
        lines.append(f"<b>{full_name}</b>")

        # Dates
        birth_year = node_data.get("birth_year")
        death_year = node_data.get("death_year")
        if birth_year or death_year:
            birth = str(birth_year) if birth_year else "?"
            death = str(death_year) if death_year else "?"
            lines.append(f"<b>Life:</b> {birth} - {death}")

        # Generation
        generation = node_data.get("generation")
        if generation is not None:
            lines.append(f"<b>Generation:</b> {generation}")

        # Partnerships
        partnerships = node_data.get("partnerships", [])
        if partnerships:
            lines.append(f"<b>Partnerships:</b> {len(partnerships)}")

        # Confidence
        confidence = node_data.get("confidence", "unknown")
        lines.append(f"<b>Confidence:</b> {confidence}")

        return "<br>".join(lines)

    def _add_surname_legend(
        self, fig: Figure, G: nx.DiGraph, color_map: Dict[int, str]
    ):
        """Add legend showing surname colors.

        Args:
            fig: Plotly figure
            G: NetworkX directed graph
            color_map: Node color mapping
        """
        # Get unique surname-color pairs
        surname_colors = {}
        for node in G.nodes:
            surname = G.nodes[node].get("surname", "Unknown")
            color = color_map.get(node)
            if surname not in surname_colors and color != self.HIGHLIGHT_COLOR:
                surname_colors[surname] = color

        # Add a dummy trace for each surname to create legend
        for surname, color in sorted(surname_colors.items())[:10]:  # Limit to 10 surnames
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=10, color=color),
                showlegend=True,
                name=surname,
            ))

    def _create_empty_figure(self, message: str) -> Figure:
        """Create an empty figure with a message.

        Args:
            message: Message to display

        Returns:
            Plotly Figure
        """
        fig = go.Figure()

        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=20, color="#64748B"),
        )

        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            plot_bgcolor="#F8FAFC",
            paper_bgcolor="white",
            height=400,
        )

        return fig

    def export_to_html(self, fig: Figure, filepath: str):
        """Export figure to HTML file.

        Args:
            fig: Plotly figure
            filepath: Output file path
        """
        fig.write_html(filepath)

    def export_to_png(self, fig: Figure, filepath: str, width: int = 1920, height: int = 1080):
        """Export figure to PNG file.

        Args:
            fig: Plotly figure
            filepath: Output file path
            width: Image width
            height: Image height
        """
        fig.write_image(filepath, width=width, height=height)
