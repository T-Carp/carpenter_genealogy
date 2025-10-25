"""Query router node for determining query type and intent."""

from typing import Any, Dict
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..database.models import QueryType, QueryIntent
from ..utils.config import Settings


class QueryRouter:
    """Routes queries to appropriate processing paths."""

    def __init__(self, settings: Settings):
        """Initialize query router.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            api_key=settings.anthropic_api_key,
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a genealogy query analyzer. Analyze the user's query and determine:
1. Query type (factual, exploratory, relationship, or timeline)
2. Entities mentioned (names, places, dates)
3. Temporal context if any

Query types:
- FACTUAL: Asks for specific facts (e.g., "When was John born?", "Where did Mary die?")
- EXPLORATORY: Asks for general information or narrative (e.g., "Tell me about...", "What do we know about...")
- RELATIONSHIP: Asks about family connections (e.g., "How is X related to Y?", "Who were X's children?")
- TIMELINE: Asks about chronology (e.g., "What happened in 1850?", "Timeline of X's life")

Return a JSON object with:
- query_type: one of [factual, exploratory, relationship, timeline]
- entities: list of entity names mentioned
- temporal_context: any time period or dates mentioned
- confidence: confidence score 0-1"""),
            ("human", "{query}"),
        ])

    async def route(self, query: str) -> QueryIntent:
        """Route a query to determine its type and extract entities.

        Args:
            query: User query string

        Returns:
            QueryIntent object with parsed information
        """
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"query": query})

        # Parse LLM response (simplified - in production, use structured output)
        content = response.content.lower()

        # Determine query type
        if "factual" in content:
            query_type = QueryType.FACTUAL
        elif "relationship" in content:
            query_type = QueryType.RELATIONSHIP
        elif "timeline" in content:
            query_type = QueryType.TIMELINE
        else:
            query_type = QueryType.EXPLORATORY

        # Simple entity extraction (in production, use NER)
        entities = []
        for word in query.split():
            if word[0].isupper() and len(word) > 2:
                entities.append(word.strip(",.?!"))

        return QueryIntent(
            original_query=query,
            query_type=query_type,
            entities=entities,
            confidence=0.8,
        )

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with query intent
        """
        import asyncio

        query = state["query"]
        intent = asyncio.run(self.route(query))

        return {
            **state,
            "query_intent": intent.model_dump(),
            "query_type": intent.query_type.value,
        }
