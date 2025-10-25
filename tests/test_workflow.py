"""Tests for LangGraph workflow."""

import pytest
from unittest.mock import Mock, patch
from src.agents.workflow import GenealogyWorkflow, GenealogyState
from src.database.vector_store import VectorStore
from src.database.structured_store import StructuredStore
from src.utils.config import Settings


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    settings = Mock(spec=Settings)
    settings.anthropic_api_key = "test-key"
    settings.claude_model = "claude-3-5-sonnet-20241022"
    settings.max_context_chunks = 5
    settings.chunk_size = 500
    settings.chunk_overlap = 50
    settings.confidence_threshold = 0.7
    return settings


@pytest.fixture
def mock_vector_store():
    """Create mock vector store."""
    return Mock(spec=VectorStore)


@pytest.fixture
def mock_structured_store():
    """Create mock structured store."""
    return Mock(spec=StructuredStore)


def test_workflow_initialization(mock_settings, mock_vector_store, mock_structured_store):
    """Test that workflow initializes correctly."""
    workflow = GenealogyWorkflow(
        mock_settings,
        mock_vector_store,
        mock_structured_store,
    )

    assert workflow.settings == mock_settings
    assert workflow.vector_store == mock_vector_store
    assert workflow.structured_store == mock_structured_store
    assert workflow.graph is not None


def test_route_after_retrieval(mock_settings, mock_vector_store, mock_structured_store):
    """Test query type routing logic."""
    workflow = GenealogyWorkflow(
        mock_settings,
        mock_vector_store,
        mock_structured_store,
    )

    # Test factual routing
    state = GenealogyState(
        query="When was John born?",
        query_type="factual",
        query_intent={},
        retrieved_docs=[],
        retrieval_count=0,
        extracted_facts=[],
        synthesized_response="",
        citations=[],
        confidence_level="",
        final_response="",
    )

    route = workflow._route_after_retrieval(state)
    assert route == "factual"

    # Test exploratory routing
    state["query_type"] = "exploratory"
    route = workflow._route_after_retrieval(state)
    assert route == "exploratory"


def test_finalize_response(mock_settings, mock_vector_store, mock_structured_store):
    """Test response finalization."""
    workflow = GenealogyWorkflow(
        mock_settings,
        mock_vector_store,
        mock_structured_store,
    )

    state = {
        "synthesized_response": "John was born in 1850.",
        "citations": [
            {
                "source_name": "Family History Book",
                "page_number": 42,
            }
        ],
        "confidence_level": "likely",
    }

    result = workflow._finalize_response(state)

    assert "John was born in 1850." in result["final_response"]
    assert "Family History Book" in result["final_response"]
    assert "p. 42" in result["final_response"]
    assert "Confidence: Likely" in result["final_response"]


# Add more tests as needed
