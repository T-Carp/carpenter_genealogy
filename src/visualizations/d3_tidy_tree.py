"""D3.js Tidy Tree visualization for family trees."""

from typing import Dict, List, Optional, Set, Any
import networkx as nx
import json


class D3TidyTreeVisualizer:
    """Visualizes family tree using D3.js Tidy Tree layout."""

    def __init__(self):
        """Initialize D3 visualizer."""
        pass

    def visualize(
        self,
        G: nx.DiGraph,
        root_person_id: Optional[int] = None,
        highlight_person_id: Optional[int] = None,
        color_by_surname: bool = True,
        title: str = "Family Tree",
    ) -> str:
        """Create D3 Tidy Tree visualization.

        Args:
            G: NetworkX directed graph from FamilyGraphBuilder
            root_person_id: Root person ID for the tree
            highlight_person_id: Person ID to highlight
            color_by_surname: Color nodes by surname
            title: Chart title

        Returns:
            HTML string with embedded D3.js visualization
        """
        if len(G.nodes) == 0:
            return self._create_empty_html("No data to display")

        # Convert graph to hierarchical tree structure
        tree_data = self._graph_to_tree(G, root_person_id)

        if not tree_data:
            return self._create_empty_html("Could not build tree structure")

        # Generate surname color map if needed
        surname_colors = {}
        if color_by_surname:
            surname_colors = self._generate_surname_colors(G)

        # Generate HTML with D3 visualization
        html = self._generate_html(
            tree_data,
            surname_colors,
            highlight_person_id,
            title,
        )

        return html

    def _graph_to_tree(
        self,
        G: nx.DiGraph,
        root_person_id: Optional[int] = None,
    ) -> Optional[Dict]:
        """Convert NetworkX graph to hierarchical tree structure.

        Args:
            G: NetworkX directed graph
            root_person_id: Root person ID (if None, finds root automatically)

        Returns:
            Hierarchical tree dict for D3
        """
        # Find root node (person with no parents)
        if root_person_id is None:
            # Find nodes with no incoming edges (no parents)
            root_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]
            if not root_nodes:
                # If no clear root (cycles), pick first node
                root_nodes = [list(G.nodes())[0]]
            root_person_id = root_nodes[0]

        # Build tree recursively
        visited = set()
        return self._build_node(G, root_person_id, visited)

    def _build_node(
        self,
        G: nx.DiGraph,
        person_id: int,
        visited: Set[int],
    ) -> Dict:
        """Recursively build tree node.

        Args:
            G: NetworkX directed graph
            person_id: Current person ID
            visited: Set of visited node IDs to prevent cycles

        Returns:
            Tree node dict
        """
        if person_id in visited:
            return None

        visited.add(person_id)

        # Get node data
        node_data = G.nodes[person_id]

        # Build node dict
        node = {
            "name": self._format_name(node_data),
            "id": person_id,
            "fullName": node_data.get("full_name", "Unknown"),
            "surname": node_data.get("surname", ""),
            "dates": node_data.get("date_str", ""),
            "birthYear": node_data.get("birth_year"),
            "deathYear": node_data.get("death_year"),
        }

        # Get children (descendants)
        children = []
        for child_id in G.successors(person_id):
            child_node = self._build_node(G, child_id, visited)
            if child_node:
                children.append(child_node)

        if children:
            node["children"] = children

        return node

    def _format_name(self, node_data: Dict) -> str:
        """Format person name for display.

        Args:
            node_data: Node data dictionary

        Returns:
            Formatted name string
        """
        given = node_data.get("given_name", "")
        surname = node_data.get("surname", "")
        dates = node_data.get("date_str", "")

        name = f"{given} {surname}"
        if dates:
            name += f" ({dates})"

        return name

    def _generate_surname_colors(self, G: nx.DiGraph) -> Dict[str, str]:
        """Generate color mapping for surnames.

        Args:
            G: NetworkX directed graph

        Returns:
            Dictionary mapping surnames to color hex codes
        """
        surnames = set()
        for node in G.nodes:
            surname = G.nodes[node].get("surname", "Unknown")
            surnames.add(surname)

        # Generate distinct colors
        colors = [
            "#1F8297",  # Teal
            "#059669",  # Green
            "#DC2626",  # Red
            "#7C3AED",  # Purple
            "#EA580C",  # Orange
            "#0891B2",  # Cyan
            "#CA8A04",  # Yellow
            "#BE123C",  # Rose
            "#4F46E5",  # Indigo
            "#16A34A",  # Emerald
        ]

        surname_colors = {}
        for i, surname in enumerate(sorted(surnames)):
            surname_colors[surname] = colors[i % len(colors)]

        return surname_colors

    def _generate_html(
        self,
        tree_data: Dict,
        surname_colors: Dict[str, str],
        highlight_person_id: Optional[int],
        title: str,
    ) -> str:
        """Generate HTML with embedded D3.js visualization.

        Args:
            tree_data: Hierarchical tree data
            surname_colors: Surname to color mapping
            highlight_person_id: Person ID to highlight
            title: Chart title

        Returns:
            HTML string
        """
        # Convert Python dict to JSON
        tree_json = json.dumps(tree_data, indent=2)
        colors_json = json.dumps(surname_colors)

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        html, body {{
            width: 100%;
            height: 100%;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #F8FAFC;
            overflow: hidden;
        }}
        #title {{
            text-align: center;
            font-size: 20px;
            font-weight: 600;
            color: #1E293B;
            padding: 15px;
            background: white;
            border-bottom: 1px solid #E2E8F0;
        }}
        #container {{
            width: 100%;
            min-height: 600px;
            height: 800px;
            background: white;
            overflow: auto;
            position: relative;
        }}
        #container svg {{
            display: block;
            margin: 0 auto;
        }}
        .node circle {{
            cursor: pointer;
            stroke: #fff;
            stroke-width: 2px;
        }}
        .node text {{
            font-size: 12px;
            font-family: sans-serif;
            cursor: pointer;
        }}
        .node.highlight circle {{
            stroke: #A855F7;
            stroke-width: 4px;
        }}
        .link {{
            fill: none;
            stroke: #94A3B8;
            stroke-opacity: 0.6;
            stroke-width: 2px;
        }}
        .tooltip {{
            position: absolute;
            padding: 10px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
        }}
    </style>
</head>
<body>
    <div id="title">{title}</div>
    <div id="container"></div>
    <div class="tooltip" id="tooltip"></div>

    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script>
        // Data
        const data = {tree_json};
        const surnameColors = {colors_json};
        const highlightId = {highlight_person_id if highlight_person_id else 'null'};

        // Get container dimensions
        const containerWidth = document.getElementById('container').clientWidth;
        const containerHeight = document.getElementById('container').clientHeight;

        // Dimensions
        const width = Math.max(1600, containerWidth);
        const marginTop = 20;
        const marginRight = 150;
        const marginBottom = 20;
        const marginLeft = 50;

        // Create hierarchy
        const root = d3.hierarchy(data);
        const dx = 30;
        const dy = 250;

        // Create tree layout
        const tree = d3.tree().nodeSize([dx, dy]);
        tree(root);

        // Compute extent
        let x0 = Infinity;
        let x1 = -Infinity;
        root.each(d => {{
            if (d.x > x1) x1 = d.x;
            if (d.x < x0) x0 = d.x;
        }});

        const height = x1 - x0 + marginTop + marginBottom;

        // Create SVG
        const svg = d3.select("#container")
            .append("svg")
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "width: 100%; height: 100%; display: block;");

        const g = svg.append("g");

        // Store initial transform
        const initialTransform = d3.zoomIdentity.translate(marginLeft, marginTop - x0);

        // Links
        g.append("g")
            .attr("fill", "none")
            .attr("stroke", "#94A3B8")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 2)
            .selectAll("path")
            .data(root.links())
            .join("path")
            .attr("class", "link")
            .attr("d", d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x));

        // Nodes
        const node = g.append("g")
            .selectAll("g")
            .data(root.descendants())
            .join("g")
            .attr("transform", d => `translate(${{d.y}},${{d.x}})`)
            .attr("class", d => d.data.id === highlightId ? "node highlight" : "node");

        // Node circles
        node.append("circle")
            .attr("r", 6)
            .attr("fill", d => {{
                const surname = d.data.surname || "Unknown";
                return surnameColors[surname] || "#64748B";
            }});

        // Node labels
        node.append("text")
            .attr("dy", "0.32em")
            .attr("x", d => d.children ? -10 : 10)
            .attr("text-anchor", d => d.children ? "end" : "start")
            .text(d => d.data.name)
            .attr("stroke", "white")
            .attr("stroke-width", 3)
            .attr("paint-order", "stroke")
            .style("font-size", "12px");

        // Tooltip
        const tooltip = d3.select("#tooltip");

        node.on("mouseover", (event, d) => {{
            tooltip.style("opacity", 1)
                .html(`
                    <strong>${{d.data.fullName}}</strong><br/>
                    ${{d.data.dates ? 'Dates: ' + d.data.dates : 'Dates unknown'}}
                `)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 10) + "px");
        }})
        .on("mouseout", () => {{
            tooltip.style("opacity", 0);
        }});

        // Make draggable/zoomable
        const zoom = d3.zoom()
            .scaleExtent([0.5, 3])
            .on("zoom", (event) => {{
                g.attr("transform", event.transform);
            }});

        svg.call(zoom).call(zoom.transform, initialTransform);
    </script>
</body>
</html>
"""
        return html

    def _create_empty_html(self, message: str) -> str:
        """Create empty HTML with message.

        Args:
            message: Message to display

        Returns:
            HTML string
        """
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #F8FAFC;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 400px;
        }}
        .message {{
            font-size: 18px;
            color: #64748B;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="message">{message}</div>
</body>
</html>
"""

    def export_to_html(self, html: str, filepath: str):
        """Export HTML to file.

        Args:
            html: HTML string
            filepath: Output file path
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
