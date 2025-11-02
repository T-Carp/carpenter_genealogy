"""Lineage tracer node for multi-generational genealogy tracing."""

from typing import Any, Dict, List, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..database.vector_store import VectorStore
from ..utils.config import Settings


class LineageTracer:
    """Traces lineages across multiple generations using iterative RAG."""

    def __init__(self, settings: Settings, vector_store: VectorStore):
        """Initialize lineage tracer.

        Args:
            settings: Application settings
            vector_store: Vector database instance
        """
        self.settings = settings
        self.vector_store = vector_store
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            api_key=settings.anthropic_api_key,
        )

        # Prompt for extracting people from query
        self.extract_people_prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract the two people mentioned in this lineage query.
Return a JSON object with:
- person1: the first person's full name
- person2: the second person's full name
- direction: "forward" if tracing descendants (person1 -> person2), "backward" if tracing ancestors (person2 <- person1)

Example:
Query: "Trace from Alexander Keenum to Nan Dee Keenum"
Response: {{"person1": "Alexander Keenum", "person2": "Nan Dee Keenum", "direction": "forward"}}"""),
            ("human", "{query}"),
        ])

        # Prompt for finding next generation
        self.find_generation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are analyzing genealogical documents to find family connections.

Look at the sources and find:
- If direction is "forward": Find the CHILDREN of the current person
- If direction is "backward": Find the PARENTS of the current person

Return ONLY the names of people found, one per line, in this exact format:

NAMES:
Full Name 1
Full Name 2
Full Name 3

If you cannot find any connections, write:
NAMES:
NONE

Do not include explanations, just the names."""),
            ("human", """Direction: {direction}
Current person: {current_person}
Target person: {target_person}

Sources:
{sources}

List the names found:"""),
        ])

    async def extract_people(self, query: str) -> Dict[str, str]:
        """Extract the two people from the lineage query.

        Args:
            query: User query

        Returns:
            Dictionary with person1, person2, and direction
        """
        import re

        # Extract full names (2-4 capitalized words together)
        # Pattern: First Middle? Last (Maiden?)
        name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b'
        matches = re.findall(name_pattern, query)

        # Filter out common false positives
        stopwords = {'Tell', 'Show', 'Trace', 'The', 'From', 'To', 'How', 'Are', 'Related'}
        names = [m for m in matches if m not in stopwords]

        # Get unique names (first and last occurrence if different)
        unique_names = []
        seen = set()
        for name in names:
            if name not in seen:
                unique_names.append(name)
                seen.add(name)

        # Determine direction
        direction = "forward"  # Default to tracing descendants
        if any(word in query.lower() for word in ["backwards", "backward", "ancestry", "ancestors", "ancestor"]):
            direction = "backward"

        person1 = unique_names[0] if len(unique_names) > 0 else ""
        person2 = unique_names[-1] if len(unique_names) > 1 else unique_names[0] if len(unique_names) == 1 else ""

        return {
            "person1": person1,
            "person2": person2,
            "direction": direction,
        }

    async def find_next_generation(
        self,
        current_person: str,
        target_person: str,
        direction: str,
        sources: str,
    ) -> Dict[str, Any]:
        """Find the next generation in the lineage.

        Args:
            current_person: Current person in the trace
            target_person: Final target person
            direction: "forward" or "backward"
            sources: Source text from vector DB

        Returns:
            Dictionary with next_generation list and metadata
        """
        chain = self.find_generation_prompt | self.llm
        response = await chain.ainvoke({
            "current_person": current_person,
            "target_person": target_person,
            "direction": direction,
            "sources": sources,
        })

        # Parse response - expect format:
        # NAMES:
        # Name 1
        # Name 2
        import re

        names = []
        content = response.content

        # Look for NAMES: section
        if "NAMES:" in content:
            # Get everything after NAMES:
            names_section = content.split("NAMES:", 1)[1]

            # Check for NONE
            if "NONE" in names_section.upper():
                return {
                    "next_generation": [],
                    "context": content,
                    "confidence": "low",
                }

            # Extract lines with names (2-4 capitalized words)
            lines = names_section.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Match full names (First Middle? Last)
                name_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})$', line)
                if name_match:
                    name = name_match.group(1)
                    # Filter out common words
                    if name not in {'None', 'The', 'And', 'Or', 'But'}:
                        names.append(name)

        confidence = "high" if names else "low"

        return {
            "next_generation": names,
            "context": content,
            "confidence": confidence,
        }

    async def trace_lineage(
        self,
        person1: str,
        person2: str,
        direction: str,
        max_iterations: int = 10,
    ) -> Dict[str, Any]:
        """Trace lineage between two people iteratively.

        Args:
            person1: Starting person
            person2: Target person
            direction: "forward" (descendants) or "backward" (ancestors)
            max_iterations: Maximum generations to search

        Returns:
            Dictionary with lineage path and metadata
        """
        lineage_path = [person1]
        current_person = person1
        iterations = 0
        all_context = []

        while iterations < max_iterations:
            iterations += 1

            # Search for information about current person - use multiple search strategies
            if direction == "forward":
                # Search for children/descendants
                search_query = f"{current_person} children son daughter born family"
            else:
                # Search for parents/ancestors
                search_query = f"{current_person} parents father mother born son daughter"

            # Retrieve relevant documents
            results = self.vector_store.search(
                search_query,
                n_results=min(self.settings.max_context_chunks, 15),  # Cap at 15 for performance
            )

            # Check if we got any results
            if not results.get("documents") or not results["documents"][0]:
                all_context.append({
                    "generation": iterations,
                    "person": current_person,
                    "findings": {"next_generation": [], "context": "No sources found", "confidence": "low"},
                })
                break

            # Compile sources - include more context
            sources_text = "\n\n".join([
                f"[Source {i+1}, page {results['metadatas'][0][i].get('page_number', '?')}]:\n{doc}"
                for i, doc in enumerate(results["documents"][0][:10])  # Limit to 10 sources
            ])

            # Find next generation
            next_gen_result = await self.find_next_generation(
                current_person=current_person,
                target_person=person2,
                direction=direction,
                sources=sources_text,
            )

            all_context.append({
                "generation": iterations,
                "person": current_person,
                "findings": next_gen_result,
            })

            # Check if we found the target
            next_generation = next_gen_result["next_generation"]

            # Look for target person in next generation - use fuzzy matching
            target_found = False
            for name in next_generation:
                # Check if this name matches the target
                # Compare last names and first names separately
                name_parts = name.split()
                target_parts = person2.split()

                # Match if:
                # 1. Full name substring match
                # 2. Last name matches (assuming last word is last name)
                # 3. First + Last name match
                if (person2.lower() in name.lower() or
                    name.lower() in person2.lower() or
                    (len(name_parts) > 0 and len(target_parts) > 0 and
                     name_parts[-1].lower() == target_parts[-1].lower() and
                     name_parts[0].lower() == target_parts[0].lower())):
                    lineage_path.append(name)
                    target_found = True
                    break

            if target_found:
                return {
                    "success": True,
                    "lineage_path": lineage_path,
                    "generations": iterations,
                    "context": all_context,
                }

            # If not found, take the first promising name and continue
            if next_generation:
                # Prefer a name that shares last name with target if possible
                target_lastname = person2.split()[-1].lower() if person2.split() else ""
                best_match = next_generation[0]  # Default to first

                if target_lastname:
                    for name in next_generation:
                        name_lastname = name.split()[-1].lower() if name.split() else ""
                        if name_lastname == target_lastname:
                            best_match = name
                            break

                current_person = best_match
                lineage_path.append(current_person)
            else:
                # No more connections found
                break

        return {
            "success": False,
            "lineage_path": lineage_path,
            "generations": iterations,
            "context": all_context,
            "message": f"Could not complete trace after {iterations} generations",
        }

    def format_lineage_response(self, trace_result: Dict[str, Any], query: str) -> str:
        """Format the lineage trace into a readable response.

        Args:
            trace_result: Result from trace_lineage
            query: Original query

        Returns:
            Formatted response string
        """
        if trace_result["success"]:
            path = trace_result["lineage_path"]
            generations = trace_result["generations"]

            response = f"**Lineage Trace:** {path[0]} → {path[-1]}\n\n"
            response += f"I found a {generations}-generation connection:\n\n"

            for i, person in enumerate(path):
                response += f"{i + 1}. **{person}**\n"

            # Add context from each generation
            response += "\n**Details from sources:**\n\n"
            for ctx in trace_result["context"]:
                response += f"Generation {ctx['generation']}: {ctx['person']}\n"
                response += f"- Found: {', '.join(ctx['findings']['next_generation']) if ctx['findings']['next_generation'] else 'No clear connections'}\n"
                response += f"- Confidence: {ctx['findings']['confidence']}\n\n"

            return response
        else:
            path = trace_result["lineage_path"]
            response = f"I attempted to trace the lineage but could not complete the full connection.\n\n"
            response += f"**Partial trace found ({len(path)} generations):**\n\n"

            for i, person in enumerate(path):
                response += f"{i + 1}. {person}\n"

            response += f"\n{trace_result.get('message', 'Unable to continue the trace.')}\n\n"
            response += "The book may not contain enough detail about intermediate generations, or the connection may require more context."

            return response

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state for LangGraph node.

        Args:
            state: Current graph state

        Returns:
            Updated state with lineage trace
        """
        import asyncio

        query = state["query"]

        # Extract people from query
        people_info = asyncio.run(self.extract_people(query))

        # Trace lineage
        trace_result = asyncio.run(self.trace_lineage(
            person1=people_info["person1"],
            person2=people_info["person2"],
            direction=people_info["direction"],
            max_iterations=8,  # Reasonable limit for genealogy
        ))

        # Format response
        lineage_response = self.format_lineage_response(trace_result, query)

        # Store in state as synthesized response
        return {
            **state,
            "synthesized_response": lineage_response,
            "retrieved_docs": state.get("retrieved_docs", []),  # Keep existing docs
            "lineage_trace": trace_result,
        }
