"""RAG retrieval node for pulling relevant content from vector database."""

from typing import Any, Dict, List
from ..database.models import RetrievalResult
from ..database.vector_store import VectorStore
from ..utils.config import Settings


class RAGRetrieval:
    """Retrieves relevant documents from vector database."""

    def __init__(self, settings: Settings, vector_store: VectorStore):
        """Initialize RAG retrieval.

        Args:
            settings: Application settings
            vector_store: Vector database instance
        """
        self.settings = settings
        self.vector_store = vector_store

    def retrieve(self, query: str, n_results: int = None) -> List[RetrievalResult]:
        """Retrieve relevant documents for a query.

        Args:
            query: Search query
            n_results: Number of results to return (defaults to max_context_chunks)

        Returns:
            List of retrieval results
        """
        if n_results is None:
            n_results = self.settings.max_context_chunks

        # Search vector database
        results = self.vector_store.search(query, n_results=n_results)

        # Convert to RetrievalResult objects
        retrieval_results = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                distance = results["distances"][0][i] if results["distances"] else 0.0

                # Convert distance to relevance score (lower distance = higher relevance)
                relevance_score = 1.0 - min(distance, 1.0)

                retrieval_results.append(
                    RetrievalResult(
                        content=doc,
                        source=metadata.get("source", "unknown"),
                        page_number=metadata.get("page_number"),
                        relevance_score=relevance_score,
                        metadata=metadata,
                    )
                )

        return retrieval_results

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with retrieved documents
        """
        query = state["query"]
        results = self.retrieve(query)

        return {
            **state,
            "retrieved_docs": [r.model_dump() for r in results],
            "retrieval_count": len(results),
        }
