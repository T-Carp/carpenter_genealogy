#!/usr/bin/env python3
"""Monitor token usage for genealogy queries."""

import os
from dotenv import load_dotenv

# Enable LangSmith tracing for token tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "genealogy-assistant"

load_dotenv()

from src.database.vector_store import VectorStore
from src.database.structured_store import StructuredStore
from src.agents.workflow import GenealogyWorkflow
from src.utils.config import get_settings


def main():
    """Run interactive query with token monitoring."""
    print("=" * 70)
    print("GENEALOGY ASSISTANT - TOKEN USAGE MONITOR")
    print("=" * 70)
    print()
    print("This tool shows detailed token usage for each workflow step.")
    print("Note: For detailed tracing, set up LangSmith (https://smith.langchain.com/)")
    print()

    # Initialize system
    settings = get_settings()
    vector_store = VectorStore(settings)
    structured_store = StructuredStore(settings)
    workflow = GenealogyWorkflow(settings, vector_store, structured_store)

    print(f"Model: {settings.claude_model}")
    print(f"Max context chunks: {settings.max_context_chunks}")
    print()

    while True:
        query = input("\n🔍 Enter your genealogy question (or 'quit' to exit): ").strip()

        if query.lower() in ["quit", "exit", "q"]:
            print("\nGoodbye!")
            break

        if not query:
            continue

        print("\n" + "=" * 70)
        print(f"PROCESSING: {query}")
        print("=" * 70)

        try:
            # Run workflow
            result = workflow.run(query)

            # Display response
            print("\n📄 RESPONSE:")
            print("-" * 70)
            print(result.get("final_response", "No response generated"))
            print("-" * 70)

            # Display token estimation
            print("\n💰 ESTIMATED TOKEN USAGE:")
            print("-" * 70)

            # Estimate based on workflow steps
            steps_with_llm = [
                ("Query Routing", 500, 100),  # Classify query type
                ("Fact Extraction", 800, 200),  # Extract facts (if factual query)
                ("Synthesis", 3000, 500),  # Main response generation
                ("Confidence Check", 800, 50),  # Assess confidence
            ]

            total_input = 0
            total_output = 0

            print(f"{'Step':<20} {'Input (est.)':<15} {'Output (est.)':<15} {'Cost (est.)'}")
            print("-" * 70)

            for step_name, input_est, output_est in steps_with_llm:
                total_input += input_est
                total_output += output_est

                # Calculate cost (Sonnet 4.5 pricing)
                cost = (input_est / 1_000_000 * 3.0) + (output_est / 1_000_000 * 15.0)

                print(f"{step_name:<20} {input_est:<15,} {output_est:<15,} ${cost:.4f}")

            print("-" * 70)
            total_cost = (total_input / 1_000_000 * 3.0) + (total_output / 1_000_000 * 15.0)
            print(f"{'TOTAL (estimated)':<20} {total_input:<15,} {total_output:<15,} ${total_cost:.4f}")

            print("\n📊 NOTE: These are estimates. Actual usage varies by:")
            print("  - Query complexity")
            print("  - Retrieved context length")
            print("  - Response detail")
            print()
            print("For exact tracking, use LangSmith:")
            print("  1. Sign up at https://smith.langchain.com/")
            print("  2. Get your API key")
            print("  3. Add to .env: LANGCHAIN_API_KEY=your_key")
            print("  4. View traces at https://smith.langchain.com/")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
