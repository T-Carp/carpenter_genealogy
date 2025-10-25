"""Fact extractor node for extracting structured facts from content."""

from typing import Any, Dict, List
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..database.models import Fact, ConfidenceLevel
from ..utils.config import Settings


class FactExtractor:
    """Extracts structured facts from genealogy content."""

    def __init__(self, settings: Settings):
        """Initialize fact extractor.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            api_key=settings.anthropic_api_key,
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a genealogy fact extractor. Extract specific genealogical facts from the provided content.

Focus on extracting:
- Birth information (date, place)
- Death information (date, place)
- Marriage information (date, place, spouse)
- Immigration/migration events
- Occupations
- Residences

For each fact, determine confidence level:
- confirmed: Explicitly stated with documentation
- likely: Strongly implied but not explicitly confirmed
- possible: Suggested but uncertain
- uncertain: Speculative or unclear

Return facts as a structured list."""),
            ("human", """Query: {query}

Content:
{content}

Extract relevant facts."""),
        ])

    async def extract(self, query: str, content: str) -> List[Dict[str, Any]]:
        """Extract facts from content.

        Args:
            query: Original user query
            content: Content to extract facts from

        Returns:
            List of extracted facts
        """
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"query": query, "content": content})

        # In production, use structured output
        # For now, return simplified structure
        facts = []

        # Parse response (simplified)
        lines = response.content.split("\n")
        for line in lines:
            if any(keyword in line.lower() for keyword in ["birth", "death", "marriage", "immigration"]):
                facts.append({
                    "description": line.strip("- "),
                    "confidence": "uncertain",
                })

        return facts

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with extracted facts
        """
        import asyncio

        query = state["query"]
        docs = state.get("retrieved_docs", [])

        # Combine document content
        content = "\n\n".join([doc["content"] for doc in docs[:3]])

        facts = asyncio.run(self.extract(query, content))

        return {
            **state,
            "extracted_facts": facts,
        }
