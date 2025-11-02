"""Fact verifier node for validating genealogical claims against sources."""

from typing import Any, Dict, List
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..utils.config import Settings


class FactVerifier:
    """Verifies genealogical claims against source documents."""

    def __init__(self, settings: Settings):
        """Initialize fact verifier.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            api_key=settings.anthropic_api_key,
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a strict fact checker for genealogical information. Your job is to verify that every claim in a response is directly supported by the source documents.

VERIFICATION PROCESS:
1. Extract each factual claim from the response (especially relationships)
2. For each claim, check if it appears EXPLICITLY in the retrieved sources
3. Mark each claim as:
   - VERIFIED: Exact quote found in sources
   - PARTIAL: Related information exists but not exact claim
   - UNVERIFIED: Claim not found in sources (likely inferred)

CRITICAL RULES:
- A relationship claim is ONLY verified if you can find the exact relationship stated in the sources
- Do NOT accept logical inferences (e.g., "if A parent of B, B parent of C, then A grandparent of C")
- Require exact quotes for verification
- Be extremely strict

Return a verification report with:
- List of verified claims (with source quotes)
- List of unverified claims that should be removed
- Corrected response with only verified information"""),
            ("human", """Original Response:
{response}

Retrieved Sources:
{sources}

Verify each claim and provide a corrected response containing ONLY verified information."""),
        ])

    async def verify(self, response: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Verify claims in a response against sources.

        Args:
            response: Generated response to verify
            sources: Retrieved source documents

        Returns:
            Dictionary with verification results and corrected response
        """
        # Format sources
        sources_text = "\n\n".join([
            f"[Source {i+1} - Page {s.get('page_number', 'Unknown')}]:\n{s.get('content', '')}"
            for i, s in enumerate(sources)
        ])

        chain = self.prompt | self.llm
        result = await chain.ainvoke({
            "response": response,
            "sources": sources_text,
        })

        # Parse the verification result
        # In production, use structured output
        corrected = result.content

        return {
            "original_response": response,
            "verified_response": corrected,
            "verification_performed": True,
        }

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with verified response
        """
        import asyncio

        response = state.get("synthesized_response", "")
        sources = state.get("retrieved_docs", [])

        if not response or not sources:
            return state

        verification = asyncio.run(self.verify(response, sources))

        return {
            **state,
            "verified_response": verification["verified_response"],
            "original_unverified_response": response,
        }
