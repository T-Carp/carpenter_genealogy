#!/usr/bin/env python3
"""Test token usage with a sample query."""

from src.database.vector_store import VectorStore
from src.database.structured_store import StructuredStore
from src.agents.workflow import GenealogyWorkflow
from src.utils.config import get_settings


def main():
    """Run a test query and estimate token usage."""
    print("=" * 70)
    print("GENEALOGY ASSISTANT - TOKEN USAGE TEST")
    print("=" * 70)
    print()

    # Initialize system
    settings = get_settings()
    vector_store = VectorStore(settings)
    structured_store = StructuredStore(settings)
    workflow = GenealogyWorkflow(settings, vector_store, structured_store)

    print(f"Model: {settings.claude_model}")
    print(f"Max context chunks: {settings.max_context_chunks}")
    print(f"Chunk size: {settings.chunk_size}")
    print()

    # Test query
    test_query = "Tell me about the Keenum family history"

    print(f"🔍 TEST QUERY: {test_query}")
    print("=" * 70)
    print()

    try:
        # Run workflow
        print("⏳ Processing query...")
        result = workflow.run(test_query)

        # Display response
        print("\n" + "=" * 70)
        print("📄 RESPONSE:")
        print("=" * 70)
        print(result.get("final_response", "No response generated"))
        print()

        # Display token estimation
        print("=" * 70)
        print("💰 ESTIMATED TOKEN USAGE:")
        print("=" * 70)
        print()

        # Estimate based on workflow steps
        steps = [
            ("1. Query Router", 600, 100, "Analyzes query type"),
            ("2. Structured DB Query", 0, 0, "Checks database (no tokens)"),
            ("3. RAG Retrieval", 0, 0, "Vector search (no tokens)"),
            ("4. Synthesizer", 3500, 600, "Generates main response"),
            ("5. Citations", 0, 0, "Formats sources (no tokens)"),
            ("6. Confidence Checker", 900, 50, "Assesses reliability"),
        ]

        total_input = 0
        total_output = 0

        print(f"{'Step':<25} {'Input':<12} {'Output':<12} {'Cost':<10} {'Description'}")
        print("-" * 95)

        for step_name, input_est, output_est, description in steps:
            if input_est > 0 or output_est > 0:
                total_input += input_est
                total_output += output_est

                # Calculate cost (Sonnet 4.5 pricing: $3/M input, $15/M output)
                cost = (input_est / 1_000_000 * 3.0) + (output_est / 1_000_000 * 15.0)

                print(f"{step_name:<25} {input_est:<12,} {output_est:<12,} ${cost:<9.4f} {description}")
            else:
                print(f"{step_name:<25} {'—':<12} {'—':<12} {'—':<10} {description}")

        print("-" * 95)
        total_cost = (total_input / 1_000_000 * 3.0) + (total_output / 1_000_000 * 15.0)
        print(f"{'TOTAL':<25} {total_input:<12,} {total_output:<12,} ${total_cost:<9.4f}")

        print()
        print("=" * 70)
        print("📊 TOKEN USAGE SUMMARY")
        print("=" * 70)
        print(f"Total Input Tokens:  {total_input:,}")
        print(f"Total Output Tokens: {total_output:,}")
        print(f"Total Tokens:        {total_input + total_output:,}")
        print(f"Estimated Cost:      ${total_cost:.4f}")
        print()
        print("💡 COST BREAKDOWN:")
        print(f"   Input:  {total_input:,} tokens × $3.00/M = ${total_input / 1_000_000 * 3.0:.4f}")
        print(f"   Output: {total_output:,} tokens × $15.00/M = ${total_output / 1_000_000 * 15.0:.4f}")
        print()

        print("📝 NOTE: These are estimates. Actual usage varies by:")
        print("   • Query complexity and length")
        print("   • Amount of retrieved context")
        print("   • Response detail and length")
        print("   • Number of sources cited")
        print()
        print("🎯 FOR EXACT TRACKING:")
        print("   Set up LangSmith (see docs/TOKEN_TRACKING.md)")
        print("   1. Sign up at https://smith.langchain.com/")
        print("   2. Add LANGCHAIN_API_KEY to .env")
        print("   3. View detailed traces online")
        print()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
