"""Citation generator node for tracking information sources."""

from typing import Any, Dict, List
from ..database.models import Citation
from ..utils.config import Settings


class CitationGenerator:
    """Generates citations for genealogical information."""

    def __init__(self, settings: Settings):
        """Initialize citation generator.

        Args:
            settings: Application settings
        """
        self.settings = settings

    def generate_citations(self, retrieved_docs: List[Dict[str, Any]]) -> List[Citation]:
        """Generate citations from retrieved documents.

        Args:
            retrieved_docs: List of retrieved document dictionaries

        Returns:
            List of Citation objects
        """
        citations = []

        for doc in retrieved_docs:
            metadata = doc.get("metadata", {})

            citation = Citation(
                source_type=metadata.get("source_type", "book"),
                source_name=metadata.get("source", "Unknown Source"),
                page_number=metadata.get("page_number"),
                section=metadata.get("section"),
                notes=f"Relevance score: {doc.get('relevance_score', 0.0):.2f}",
            )

            citations.append(citation)

        return citations

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with citations
        """
        docs = state.get("retrieved_docs", [])
        citations = self.generate_citations(docs)

        return {
            **state,
            "citations": [c.model_dump() for c in citations],
        }
