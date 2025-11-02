"""Confidence checker node for assessing information reliability."""

from typing import Any, Dict, List
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..database.models import ConfidenceLevel
from ..utils.config import Settings


class ConfidenceChecker:
    """Assesses confidence levels for genealogical information."""

    def __init__(self, settings: Settings):
        """Initialize confidence checker.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            api_key=settings.anthropic_api_key,
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a genealogy confidence assessor. Evaluate the reliability of information based on the available sources.

Confidence levels:
- CONFIRMED: Multiple independent sources confirm the information, or direct quotes from primary sources
- LIKELY: Information is clearly stated in at least one reliable source with no contradictions
- POSSIBLE: Information is suggested or mentioned but not explicitly confirmed
- UNCERTAIN: Information is inferred, not directly stated in sources, or has conflicting evidence

When assessing:
1. Are facts explicitly stated in sources or inferred?
2. How many sources confirm the information?
3. Are there any contradictions?
4. Are direct quotes provided?

If information is inferred rather than explicitly stated, mark as UNCERTAIN."""),
            ("human", """Response: {response}

Retrieved sources: {sources}

What is the overall confidence level for this information?
Return only one word: CONFIRMED, LIKELY, POSSIBLE, or UNCERTAIN"""),
        ])

    async def assess_confidence(
        self,
        response: str,
        sources: List[Dict[str, Any]],
    ) -> ConfidenceLevel:
        """Assess confidence level for a response.

        Args:
            response: Generated response
            sources: Retrieved source documents

        Returns:
            Confidence level
        """
        # Format sources
        sources_text = "\n".join([
            f"- {s.get('source', 'Unknown')} (relevance: {s.get('relevance_score', 0):.2f})"
            for s in sources
        ])

        chain = self.prompt | self.llm
        result = await chain.ainvoke({
            "response": response,
            "sources": sources_text,
        })

        # Parse confidence level
        content = result.content.upper().strip()
        if "CONFIRMED" in content:
            return ConfidenceLevel.CONFIRMED
        elif "LIKELY" in content:
            return ConfidenceLevel.LIKELY
        elif "POSSIBLE" in content:
            return ConfidenceLevel.POSSIBLE
        else:
            return ConfidenceLevel.UNCERTAIN

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with confidence assessment
        """
        import asyncio

        response = state.get("synthesized_response", "")
        sources = state.get("retrieved_docs", [])

        confidence = asyncio.run(self.assess_confidence(response, sources))

        return {
            **state,
            "confidence_level": confidence.value,
        }
