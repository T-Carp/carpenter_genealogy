"""LangGraph workflow for genealogy analysis."""

from typing import Any, Dict, TypedDict
from langgraph.graph import StateGraph, END

from .query_router import QueryRouter
from .rag_retrieval import RAGRetrieval
from .fact_extractor import FactExtractor
from .synthesizer import Synthesizer
from .citation_generator import CitationGenerator
from .confidence_checker import ConfidenceChecker
from .structured_query import StructuredQuery
from ..database.vector_store import VectorStore
from ..database.structured_store import StructuredStore
from ..utils.config import Settings
from ..utils.token_tracker import TokenTracker


class GenealogyState(TypedDict):
    """State for the genealogy workflow."""

    query: str
    query_intent: Dict[str, Any]
    query_type: str
    structured_response: str
    has_structured_data: bool
    retrieved_docs: list[Dict[str, Any]]
    retrieval_count: int
    extracted_facts: list[Dict[str, Any]]
    synthesized_response: str
    verified_response: str
    original_unverified_response: str
    citations: list[Dict[str, Any]]
    confidence_level: str
    final_response: str
    token_usage: Dict[str, Any]  # Track token usage per step


class GenealogyWorkflow:
    """LangGraph workflow for answering genealogy queries."""

    def __init__(
        self,
        settings: Settings,
        vector_store: VectorStore,
        structured_store: StructuredStore,
    ):
        """Initialize workflow.

        Args:
            settings: Application settings
            vector_store: Vector database instance
            structured_store: Structured database instance
        """
        self.settings = settings
        self.vector_store = vector_store
        self.structured_store = structured_store

        # Initialize nodes
        self.query_router = QueryRouter(settings)
        self.structured_query = StructuredQuery(settings, structured_store)
        self.rag_retrieval = RAGRetrieval(settings, vector_store)
        self.fact_extractor = FactExtractor(settings)
        self.synthesizer = Synthesizer(settings)
        self.citation_generator = CitationGenerator(settings)
        self.confidence_checker = ConfidenceChecker(settings)

        # Build graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow.

        Returns:
            Compiled workflow graph
        """
        # Create graph
        workflow = StateGraph(GenealogyState)

        # Add nodes
        workflow.add_node("route_query", self.query_router)
        workflow.add_node("query_structured_db", self.structured_query)
        workflow.add_node("retrieve_docs", self.rag_retrieval)
        workflow.add_node("extract_facts", self.fact_extractor)
        workflow.add_node("synthesize", self.synthesizer)
        workflow.add_node("generate_citations", self.citation_generator)
        workflow.add_node("check_confidence", self.confidence_checker)
        workflow.add_node("finalize", self._finalize_response)

        # Define edges
        workflow.set_entry_point("route_query")

        # Route query -> Try structured DB first
        workflow.add_edge("route_query", "query_structured_db")

        # After structured query -> Always retrieve RAG docs for additional context
        workflow.add_edge("query_structured_db", "retrieve_docs")

        # After retrieval, branch based on query type
        workflow.add_conditional_edges(
            "retrieve_docs",
            self._route_after_retrieval,
            {
                "factual": "extract_facts",
                "exploratory": "synthesize",
                "relationship": "synthesize",
                "timeline": "synthesize",
            },
        )

        # Factual path: Extract facts -> Synthesize
        workflow.add_edge("extract_facts", "synthesize")

        # After synthesis, generate citations
        workflow.add_edge("synthesize", "generate_citations")

        # After citations, check confidence
        workflow.add_edge("generate_citations", "check_confidence")

        # After confidence check, finalize
        workflow.add_edge("check_confidence", "finalize")

        # Finalize ends the workflow
        workflow.add_edge("finalize", END)

        return workflow.compile()

    def _route_after_retrieval(self, state: GenealogyState) -> str:
        """Route to appropriate node after retrieval.

        Args:
            state: Current state

        Returns:
            Next node name
        """
        query_type = state.get("query_type", "exploratory")
        return query_type

    def _finalize_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize the response with all components.

        Args:
            state: Current state

        Returns:
            Updated state with final response
        """
        # Use synthesized response
        response = state.get("synthesized_response", "")

        # If we have structured DB data, prepend it
        structured_response = state.get("structured_response")
        if structured_response:
            response = structured_response + "\n\n" + response

        citations = state.get("citations", [])
        confidence = state.get("confidence_level", "uncertain")

        # Format final response
        final_response = response

        # Add citation section if available
        if citations:
            final_response += "\n\n**Sources:**\n"
            for i, citation in enumerate(citations[:5], 1):  # Limit to top 5
                source = citation.get("source_name", "Unknown")
                page = citation.get("page_number")
                final_response += f"{i}. {source}"
                if page:
                    final_response += f", p. {page}"
                final_response += "\n"

        # Add confidence note
        final_response += f"\n*Confidence: {confidence.title()}*"

        return {
            **state,
            "final_response": final_response,
        }

    async def arun(self, query: str) -> Dict[str, Any]:
        """Run the workflow asynchronously.

        Args:
            query: User query

        Returns:
            Final state with response
        """
        initial_state = GenealogyState(
            query=query,
            query_intent={},
            query_type="",
            structured_response="",
            has_structured_data=False,
            retrieved_docs=[],
            retrieval_count=0,
            extracted_facts=[],
            synthesized_response="",
            verified_response="",
            original_unverified_response="",
            citations=[],
            confidence_level="",
            final_response="",
        )

        result = await self.graph.ainvoke(initial_state)
        return result

    def run(self, query: str) -> Dict[str, Any]:
        """Run the workflow synchronously.

        Args:
            query: User query

        Returns:
            Final state with response
        """
        import asyncio

        return asyncio.run(self.arun(query))
