"""Advanced relationship extraction using LLM."""

from typing import List, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..database.structured_store import StructuredStore
from ..database.models import ConfidenceLevel
from ..utils.config import Settings


class RelationshipExtractor:
    """Extracts family relationships from text using LLM."""

    def __init__(self, settings: Settings, structured_store: StructuredStore):
        """Initialize relationship extractor.

        Args:
            settings: Application settings
            structured_store: Structured database instance
        """
        self.settings = settings
        self.structured_store = structured_store
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            api_key=settings.anthropic_api_key,
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a genealogy data extraction expert. Extract ONLY explicitly stated family relationships from the text.

Extract information in this format for each person and relationship found:

PERSONS:
- Full Name: [exact name as written]
- Birth Date: [if mentioned]
- Birth Place: [if mentioned]
- Death Date: [if mentioned]
- Death Place: [if mentioned]
- Page Reference: [page number]

RELATIONSHIPS:
- Person 1: [full name]
- Person 2: [full name]
- Relationship: [parent, child, spouse, sibling - be specific]
- Exact Quote: "[quote the sentence that states this relationship]"
- Page Reference: [page number]

CRITICAL RULES:
1. ONLY extract relationships that are EXPLICITLY stated
2. Use exact names as they appear in text
3. Include the exact sentence that proves each relationship
4. If a relationship is implied but not stated, DO NOT include it
5. Be conservative - better to miss a relationship than to infer one

Example of GOOD extraction:
Text: "John Smith married Mary Jones in 1850. They had three children: Sarah, Robert, and William."
- Person 1: John Smith | Person 2: Mary Jones | Relationship: spouse | Quote: "John Smith married Mary Jones in 1850"
- Person 1: John Smith | Person 2: Sarah | Relationship: parent | Quote: "They had three children: Sarah, Robert, and William"

Example of BAD extraction (DO NOT DO THIS):
Text: "John Smith's grandson visited in 1920."
- DO NOT extract: Person 1: John Smith | Person 2: [unknown] | Relationship: grandparent
- REASON: The grandson is not named, so we cannot create a verifiable relationship"""),
            ("human", """Extract all persons and relationships from this genealogy text:

{text}

Page number: {page_number}"""),
        ])

    async def extract_from_text(
        self,
        text: str,
        page_number: int,
        source_name: str,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Extract persons and relationships from text.

        Args:
            text: Text to extract from
            page_number: Page number for reference
            source_name: Name of the source document

        Returns:
            Dictionary with 'persons' and 'relationships' lists
        """
        chain = self.prompt | self.llm
        result = await chain.ainvoke({
            "text": text,
            "page_number": page_number,
        })

        # Parse the result (simplified - in production use structured output)
        content = result.content

        # For now, return the raw extraction
        # In production, parse this into structured data
        return {
            "raw_extraction": content,
            "page_number": page_number,
            "source_name": source_name,
        }

    def process_page_batch(
        self,
        pages: List[tuple[str, int]],
        source_name: str,
    ) -> List[Dict[str, Any]]:
        """Process multiple pages and extract relationships.

        Args:
            pages: List of (text, page_number) tuples
            source_name: Name of source document

        Returns:
            List of extraction results
        """
        import asyncio

        async def process_all():
            tasks = [
                self.extract_from_text(text, page_num, source_name)
                for text, page_num in pages
                if len(text.strip()) > 100  # Only process pages with substantial content
            ]
            return await asyncio.gather(*tasks)

        return asyncio.run(process_all())

    def store_extracted_relationships(
        self,
        extractions: List[Dict[str, Any]],
    ) -> Dict[str, int]:
        """Store extracted relationships in structured database.

        Args:
            extractions: List of extraction results

        Returns:
            Statistics about what was stored
        """
        stats = {
            "persons_added": 0,
            "relationships_added": 0,
            "pages_processed": len(extractions),
        }

        # In production, parse the LLM output and store in database
        # For now, just log the extractions
        print(f"\nProcessed {len(extractions)} pages for relationship extraction")
        print("Note: Full parsing and storage not yet implemented")
        print("Extractions are available in the vector database")

        return stats
