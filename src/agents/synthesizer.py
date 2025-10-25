"""Synthesizer node for creating narrative responses from multiple sources."""

from typing import Any, Dict
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..utils.config import Settings


class Synthesizer:
    """Synthesizes narrative responses from retrieved information."""

    def __init__(self, settings: Settings):
        """Initialize synthesizer.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            api_key=settings.anthropic_api_key,
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful genealogy assistant that provides clear, accurate information about family history based on available sources.

When responding:
- Provide information in a clear, conversational manner
- Only state facts that are explicitly mentioned in the sources
- If making connections or inferences, clearly indicate this with phrases like "This suggests..." or "It appears..."
- When information is uncertain or missing, acknowledge this directly
- Include relevant quotes from sources when appropriate
- Organize information logically and clearly

Your goal is to help users understand their family history accurately while being conversational and helpful."""),
            ("human", """Query: {query}

Retrieved Information:
{context}

Based on the sources provided, please answer the user's question."""),
        ])

    async def synthesize(self, query: str, context: str) -> str:
        """Synthesize a narrative response.

        Args:
            query: Original user query
            context: Retrieved context from documents

        Returns:
            Synthesized narrative response
        """
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"query": query, "context": context})

        return response.content

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with synthesized response
        """
        import asyncio

        query = state["query"]
        docs = state.get("retrieved_docs", [])

        # Build context from retrieved documents
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.get("source", "Unknown")
            page = doc.get("page_number", "")
            content = doc.get("content", "")
            score = doc.get("relevance_score", 0.0)

            context_parts.append(
                f"[Source {i}: {source}" + (f", p. {page}" if page else "") + f" (relevance: {score:.2f})]\n{content}"
            )

        context = "\n\n".join(context_parts)

        response = asyncio.run(self.synthesize(query, context))

        return {
            **state,
            "synthesized_response": response,
        }
