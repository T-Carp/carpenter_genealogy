"""Gradio web interface for genealogy chat."""

import gradio as gr
from pathlib import Path
from typing import List, Tuple

from ..agents.workflow import GenealogyWorkflow
from ..database.vector_store import VectorStore
from ..database.structured_store import StructuredStore
from ..utils.config import Settings, get_settings


class GenealogyChat:
    """Chat interface for genealogy queries."""

    def __init__(self):
        """Initialize the chat interface."""
        self.settings = get_settings()
        self.vector_store = VectorStore(self.settings)
        self.structured_store = StructuredStore(self.settings)
        self.workflow = GenealogyWorkflow(
            self.settings,
            self.vector_store,
            self.structured_store,
        )

    def chat(
        self,
        message: str,
        history: List,
    ) -> Tuple[List, str]:
        """Process a chat message.

        Args:
            message: User message
            history: Chat history (list of message dicts)

        Returns:
            Tuple of (updated history, empty string to clear input)
        """
        if not message.strip():
            return history, ""

        # Run workflow
        try:
            result = self.workflow.run(message)
            response = result.get("final_response", "I couldn't process that query.")
        except Exception as e:
            response = f"An error occurred: {str(e)}"

        # Update history with new message format (for Gradio 5.x)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return history, ""

    def get_stats(self) -> str:
        """Get database statistics.

        Returns:
            Formatted statistics string
        """
        try:
            vector_stats = self.vector_store.get_stats()
            return f"""**Database Statistics**

Vector Database:
- Collection: {vector_stats['collection_name']}
- Documents: {vector_stats['document_count']}
- Embedding Model: {vector_stats['embedding_model']}

Structured Database:
- Location: {self.settings.structured_db_path}
"""
        except Exception as e:
            return f"Error getting statistics: {str(e)}"


def create_gradio_interface() -> gr.Blocks:
    """Create the Gradio interface.

    Returns:
        Gradio Blocks interface
    """
    chat_instance = GenealogyChat()

    with gr.Blocks(
        title="Carpenter Family Genealogy Assistant",
        theme=gr.themes.Soft(),
    ) as interface:
        gr.Markdown("""
        # Family Genealogy Assistant

        Ask questions about your family history and get AI-powered answers with citations.

        **Example queries for lineage tracing:**
        - "Trace the lineage from Alexander Keenum down to his descendants. Show me how the family line progressed through each generation."
        - "Trace Nan Dee Keenum's ancestry backwards to Alexander Keenum. Show me all the generations connecting them."
        - "Who are the earliest Keenum ancestors mentioned in the book?"
        - "Tell me about the descendants of Alexander Keenum. Who are their children, grandchildren, and great-grandchildren?"
        - "How are Alexander Keenum and Nan Dee Keenum related? Show me the complete family connection."
        """)

        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(
                label="Genealogy Chat",
                height=500,
                type="messages",
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask about your family history...",
                    scale=4,
                )
                submit = gr.Button("Send", scale=1, variant="primary")

            clear = gr.Button("Clear History")

            # Chat interaction
            msg.submit(
                chat_instance.chat,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg],
            )

            submit.click(
                chat_instance.chat,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg],
            )

            clear.click(lambda: [], outputs=[chatbot])

        with gr.Tab("Database Info"):
            stats_output = gr.Markdown()
            stats_button = gr.Button("Refresh Statistics")

            stats_button.click(
                chat_instance.get_stats,
                outputs=[stats_output],
            )

            # Load stats on page load
            interface.load(
                chat_instance.get_stats,
                outputs=[stats_output],
            )

        with gr.Tab("About"):
            gr.Markdown("""
            ## About This System

            This genealogy assistant uses:

            ### LangGraph Workflow
            The system uses a sophisticated LangGraph workflow with multiple specialized nodes:

            1. **Query Router**: Analyzes your question to determine the best processing path
            2. **RAG Retrieval**: Searches the vector database for relevant narrative content
            3. **Fact Extractor**: Extracts structured facts for factual queries
            4. **Synthesizer**: Creates comprehensive narrative responses
            5. **Citation Generator**: Tracks and cites information sources
            6. **Confidence Checker**: Assesses reliability of information

            ### Hybrid Database Approach

            - **Vector Database**: Stores narrative content for semantic search
            - **Structured Database**: Stores facts, relationships, and citations

            ### Claude API

            This system uses Anthropic's Claude API for natural language processing.

            **Configuration:**
            - Model: Claude 3.5 Sonnet
            - Embeddings: sentence-transformers/all-MiniLM-L6-v2

            ### Confidence Levels

            Responses include confidence indicators:
            - **Confirmed**: Multiple reliable sources
            - **Likely**: Strong evidence
            - **Possible**: Some evidence
            - **Uncertain**: Weak or conflicting evidence

            ---

            For technical documentation, see the project README and CLAUDE.md files.
            """)

    return interface


def launch_app(share: bool = False, server_port: int = 7860):
    """Launch the Gradio application.

    Args:
        share: Whether to create a public share link
        server_port: Port to run the server on
    """
    interface = create_gradio_interface()
    interface.launch(
        share=share,
        server_port=server_port,
        server_name="0.0.0.0",
    )


if __name__ == "__main__":
    launch_app()
