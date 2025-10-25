# Carpenter Family Genealogy Assistant

An AI-powered genealogy analysis system that uses LangGraph workflows and RAG (Retrieval Augmented Generation) to answer questions about family history. Built with Claude 3.5 Sonnet and designed specifically for analyzing genealogical documents.

## Features

- **LangGraph Workflow**: Sophisticated multi-node processing pipeline
  - Query routing (factual vs exploratory vs relationship vs timeline)
  - RAG retrieval from vector database
  - Fact extraction for structured queries
  - Response synthesis across multiple sources
  - Automatic citation generation
  - Confidence assessment

- **Hybrid Database Architecture**:
  - **Vector Database** (ChromaDB): Narrative content with semantic search
  - **Structured Database** (SQLite): Facts, relationships, dates, and citations

- **Interactive Chat Interface**: Gradio-based web UI with chat history

- **PDF Ingestion Pipeline**: Converts genealogy books into searchable databases

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/carpenter_genealogy.git
cd carpenter_genealogy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Ingest PDF Documents

Place your genealogy PDF in the `data/pdfs/` directory, then run:

```bash
python ingest_pdf.py data/pdfs/your_genealogy_book.pdf
```

Or process an entire directory:

```bash
python ingest_pdf.py data/pdfs/
```

### 4. Launch the Application

```bash
python app.py
```

Visit http://localhost:7860 in your browser.

## Usage

### Chat Interface

Ask questions about your family history:

**Factual Queries:**
- "When was John Carpenter born?"
- "Where did Mary Smith die?"
- "What was Thomas's occupation?"

**Exploratory Queries:**
- "Tell me about the Carpenter family's immigration story"
- "What do we know about family members in the 1800s?"
- "Describe the family's life in Pennsylvania"

**Relationship Queries:**
- "How is Mary related to John?"
- "Who were Sarah's children?"
- "Show me the family tree for Thomas"

**Timeline Queries:**
- "What happened in 1850?"
- "Give me a timeline of John's life"
- "What events occurred during the Civil War?"

### Command Line Options

```bash
# Run with custom port
python app.py --port 8080

# Create public share link
python app.py --share
```

## Architecture

### LangGraph Workflow

The system uses a state machine workflow with conditional routing:

```
Query → Route Query → Retrieve Docs → [Branch by type]
                                    ↓
        Factual: Extract Facts → Synthesize
        Other: Synthesize
                                    ↓
        Generate Citations → Check Confidence → Finalize
```

### Database Design

**Vector Database (ChromaDB):**
- Stores narrative content chunks
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Metadata: source, page number, section

**Structured Database (SQLite):**
- `persons`: Names, dates, places
- `relationships`: Family connections
- `facts`: Birth, death, marriage, immigration events
- `citations`: Source references

### Confidence Levels

All information includes confidence assessment:
- **Confirmed**: Multiple reliable sources, primary documentation
- **Likely**: Strong evidence, consistent across sources
- **Possible**: Some evidence, mentions but not confirmed
- **Uncertain**: Weak evidence, conflicting sources

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black .

# Lint code
ruff check .
```

### Project Structure

```
carpenter_genealogy/
├── src/
│   ├── agents/          # LangGraph workflow nodes
│   │   ├── query_router.py
│   │   ├── rag_retrieval.py
│   │   ├── fact_extractor.py
│   │   ├── synthesizer.py
│   │   ├── citation_generator.py
│   │   ├── confidence_checker.py
│   │   └── workflow.py
│   ├── database/        # Database interfaces
│   │   ├── models.py
│   │   ├── vector_store.py
│   │   └── structured_store.py
│   ├── processors/      # Document processing
│   │   └── pdf_processor.py
│   ├── ui/              # User interface
│   │   └── gradio_app.py
│   └── utils/           # Configuration
│       └── config.py
├── data/
│   ├── pdfs/           # Source PDFs
│   ├── vector_store/   # ChromaDB data
│   └── structured_db/  # SQLite database
├── tests/              # Test files
├── app.py              # Main application
├── ingest_pdf.py       # PDF ingestion script
└── requirements.txt
```

## Claude API Setup

This system uses the Anthropic Claude API. To get an API key:

1. Visit https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Add it to your `.env` file

**Model Configuration:**
- Default model: `claude-3-5-sonnet-20241022`
- Supports all Claude 3 models
- Can be changed in `.env` file

**API Usage Notes:**
- The system makes multiple API calls per query (routing, extraction, synthesis, confidence)
- Costs vary based on input/output tokens
- Consider implementing caching for repeated queries
- Monitor usage in the Anthropic Console

## Future Integrations

### Additional Data Sources

The system is designed to integrate with external genealogy databases:

**Planned Integrations:**
1. **Ancestry.com API**
   - Cross-reference family trees
   - Access historical records
   - Validate dates and relationships

2. **FamilySearch API**
   - Access historical documents
   - Find additional family members
   - Verify genealogical connections

3. **Findagrave.com**
   - Cemetery records
   - Burial locations
   - Memorial photographs

4. **Historical Records APIs**
   - Census data
   - Immigration records
   - Military service records

**Implementation Approach:**

```python
# Example integration node
class ExternalSourceRetrieval:
    async def search_ancestry(self, person_name, birth_year):
        # Query Ancestry.com API
        pass

    async def search_familysearch(self, person_name, location):
        # Query FamilySearch API
        pass
```

Add as additional nodes in the LangGraph workflow to cross-reference external data with your local database.

### Knowledge Graph Option

For complex family relationships, consider Neo4j:

```bash
# Install Neo4j
docker run -d \
  --name neo4j-genealogy \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest

# Configure in .env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

This enables powerful relationship queries like "Find all ancestors who immigrated from Ireland."

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [Anthropic Claude](https://www.anthropic.com/claude)
- UI with [Gradio](https://gradio.app/)
- Vector database: [ChromaDB](https://www.trychroma.com/)
