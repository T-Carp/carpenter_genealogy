# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered genealogy analysis system for the Carpenter family using LangGraph workflows, RAG (Retrieval Augmented Generation), and Claude 3.5 Sonnet. The system converts genealogy PDF documents into a searchable database and provides an interactive chat interface for querying family history.

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY
```

### Running the Application
```bash
# Start the Gradio web interface (default port 7860)
python app.py

# Custom port
python app.py --port 8080

# Create public share link
python app.py --share
```

### PDF Ingestion
```bash
# Ingest a single PDF
python ingest_pdf.py data/pdfs/genealogy_book.pdf

# Ingest all PDFs in directory
python ingest_pdf.py data/pdfs/

# With custom source name
python ingest_pdf.py data/pdfs/book.pdf --source-name "Family History Vol 1"
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_workflow.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Format code
black .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

## Architecture

### High-Level Overview

The system uses a **hybrid database approach** with **LangGraph workflow orchestration**:

1. **Ingestion Pipeline**: PDFs → Text extraction → Chunking → Vector DB + Structured DB
2. **Query Processing**: User query → LangGraph workflow → Response with citations
3. **User Interface**: Gradio chat interface with real-time responses

### LangGraph Workflow

The core of the system is a LangGraph state machine that processes queries through specialized nodes:

**Workflow Graph** (`src/agents/workflow.py`):
```
Entry: Query
  ↓
QueryRouter (determines query type: factual/exploratory/relationship/timeline)
  ↓
RAGRetrieval (searches vector DB for relevant content)
  ↓
[Conditional branch based on query type]
  ├─ Factual → FactExtractor (extracts structured data)
  └─ Other types → skip to Synthesizer
  ↓
Synthesizer (creates narrative response from sources)
  ↓
CitationGenerator (tracks information sources)
  ↓
ConfidenceChecker (assesses reliability: confirmed/likely/possible/uncertain)
  ↓
Finalize (formats final response with citations and confidence)
  ↓
End
```

**Key Design Principle**: Each node is a self-contained function that takes `state: Dict` and returns updated `state: Dict`, enabling flexible composition and testing.

### Agent Nodes

All nodes in `src/agents/`:

- **QueryRouter** (`query_router.py`): Uses Claude to analyze query intent and classify type
- **RAGRetrieval** (`rag_retrieval.py`): Semantic search in ChromaDB, returns top-k chunks
- **FactExtractor** (`fact_extractor.py`): Extracts structured facts (dates, places, events)
- **Synthesizer** (`synthesizer.py`): Creates coherent narrative from multiple sources
- **CitationGenerator** (`citation_generator.py`): Generates source references
- **ConfidenceChecker** (`confidence_checker.py`): Assesses information reliability

### Database Architecture

**Hybrid Approach** - Different data types stored optimally:

**Vector Database** (`src/database/vector_store.py`):
- **Technology**: ChromaDB with persistent storage
- **Purpose**: Narrative content for semantic search
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Chunking**: RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
- **Metadata**: source, page_number, section, source_type
- **Location**: `data/vector_store/`

**Structured Database** (`src/database/structured_store.py`):
- **Technology**: SQLite with SQLAlchemy ORM
- **Purpose**: Facts, relationships, citations with precise lookups
- **Schema**:
  - `persons`: id, first_name, middle_name, last_name, maiden_name, birth_date, birth_place, death_date, death_place, gender, confidence
  - `relationships`: id, person1_id, person2_id, relationship_type, confidence
  - `facts`: id, person_id, fact_type, date, place, description, confidence, citation_id
  - `citations`: id, source_type, source_name, page_number, section, url, notes
- **Location**: `data/structured_db/genealogy.db`

**Why Hybrid?**
- Factual queries ("When was John born?") → Fast SQL lookup
- Semantic queries ("Tell me about immigration") → Vector similarity search
- Best of both worlds for genealogical research

### Data Models

**Pydantic Models** (`src/database/models.py`):

Key models that define the system's data structures:
- `Person`, `Relationship`, `Citation`, `Fact`: Genealogical entities
- `ConfidenceLevel` (Enum): confirmed | likely | possible | uncertain
- `QueryType` (Enum): factual | exploratory | relationship | timeline
- `QueryIntent`: Parsed user query with entities and context
- `RetrievalResult`: Document chunk with relevance score
- `GenealogyResponse`: Final response with answer, confidence, citations

**Important**: All database operations use these models for type safety and validation.

### PDF Processing Pipeline

**PDFProcessor** (`src/processors/pdf_processor.py`):

1. **Extraction**: Uses PyMuPDF (fitz) for text extraction with page numbers
2. **Chunking**: RecursiveCharacterTextSplitter maintains context across chunks
3. **Vector Indexing**: Embeddings generated and stored in ChromaDB
4. **Structured Extraction**: Pattern matching for dates, events (basic - can be enhanced with NER)

**Processing Flow**:
```
PDF → extract_text_from_pdf() → [(text, page_num), ...]
    → chunk_text() → [(chunk, metadata), ...]
    → add_documents() → Vector DB
    → extract_structured_data() → Structured DB
```

### Configuration Management

**Settings** (`src/utils/config.py`):

Uses Pydantic Settings for environment-based configuration:
- Loads from `.env` file
- Type validation
- Default values
- Access via `get_settings()`

**Key Settings**:
- `anthropic_api_key`: Claude API key
- `claude_model`: Model name (default: claude-3-5-sonnet-20241022)
- `max_context_chunks`: Number of chunks to retrieve (default: 10)
- `chunk_size`, `chunk_overlap`: Text splitting parameters
- `confidence_threshold`: Minimum confidence for responses

### UI Layer

**Gradio Interface** (`src/ui/gradio_app.py`):

Three-tab interface:
1. **Chat**: Main conversation interface with history
2. **Database Info**: Statistics about indexed content
3. **About**: System documentation and API info

**Key Features**:
- Persistent chat history within session
- Real-time response generation
- Citation display in responses
- Confidence indicators

## Common Development Tasks

### Adding a New Workflow Node

1. Create node class in `src/agents/your_node.py`:
```python
class YourNode:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = ChatAnthropic(...)

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Process state
        return {**state, "new_field": value}
```

2. Register in workflow (`src/agents/workflow.py`):
```python
workflow.add_node("your_node", self.your_node)
workflow.add_edge("previous_node", "your_node")
```

### Adding New Database Fields

1. Update Pydantic model in `src/database/models.py`
2. Update SQLAlchemy model in `src/database/structured_store.py`
3. Add migration or drop/recreate database for testing

### Modifying Chunking Strategy

Edit `src/processors/pdf_processor.py`:
```python
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size,  # Adjust in .env
    chunk_overlap=settings.chunk_overlap,
    separators=["\n\n", "\n", ". ", " "],  # Customize here
)
```

### Changing Embedding Model

Edit `src/database/vector_store.py`:
```python
self.embedding_model = SentenceTransformer("your-model-name")
```

Popular alternatives:
- `all-mpnet-base-v2`: Higher quality, slower
- `paraphrase-MiniLM-L6-v2`: Paraphrase detection
- `multi-qa-MiniLM-L6-cos-v1`: Optimized for Q&A

## Important Patterns

### Async/Sync Handling

Many nodes use async Claude API calls but are wrapped for sync LangGraph:
```python
def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
    import asyncio
    result = asyncio.run(self.async_method(state))
    return {**state, "result": result}
```

### State Management

LangGraph state is a dictionary that flows through nodes. Always:
- Include all previous state: `{**state, new_field: value}`
- Use typed hints: `GenealogyState(TypedDict)`
- Document expected state fields

### Error Handling

Critical points for error handling:
1. PDF processing: File I/O, corrupt PDFs
2. API calls: Rate limits, network issues
3. Database operations: Missing data, schema changes

## Testing Strategy

### Unit Tests
- Test individual nodes with mock state
- Test database operations with temporary DBs
- Test PDF processing with sample files

### Integration Tests
- Test full workflow end-to-end
- Test PDF ingestion pipeline
- Test UI interactions

### Test Data
Place test PDFs in `tests/fixtures/`

## Deployment Considerations

### Environment Variables
Ensure `.env` is never committed. Use environment-specific configs:
- `.env.development`
- `.env.production`

### Database Persistence
Both databases are file-based:
- Vector DB: `data/vector_store/` (directory)
- Structured DB: `data/structured_db/genealogy.db` (single file)

Backup strategy: Regular backups of both directories

### API Key Security
- Use separate API keys for dev/prod
- Implement rate limiting
- Monitor usage in Anthropic Console

## Future Enhancement Areas

Based on prompt requirements:

1. **Enhanced Structured Extraction**: Replace regex with NER models for entity extraction
2. **Knowledge Graph**: Implement Neo4j integration for complex relationship queries
3. **External Data Sources**: Add nodes for Ancestry.com, FamilySearch APIs
4. **Caching Layer**: Implement query caching to reduce API costs
5. **Multi-source Verification**: Cross-reference information across multiple sources
6. **Timeline Visualization**: Generate visual timelines and family trees
7. **Export Functionality**: GEDCOM export for compatibility with other tools

## Troubleshooting

### Database Issues
```bash
# Reset vector database
rm -rf data/vector_store/*

# Reset structured database
rm data/structured_db/genealogy.db

# Re-ingest PDFs
python ingest_pdf.py data/pdfs/
```

### API Issues
- Check API key in `.env`
- Verify model name is correct
- Check Anthropic API status: https://status.anthropic.com/

### Import Errors
```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Key Files Reference

**Entry Points**:
- `app.py`: Main application (Gradio UI)
- `ingest_pdf.py`: PDF ingestion script

**Core Logic**:
- `src/agents/workflow.py`: LangGraph orchestration
- `src/database/vector_store.py`: Vector search
- `src/database/structured_store.py`: SQL operations
- `src/processors/pdf_processor.py`: Document processing

**Configuration**:
- `.env`: Environment variables (not in git)
- `src/utils/config.py`: Settings management

**Documentation**:
- `README.md`: User-facing documentation
- `docs/CLAUDE_API_GUIDE.md`: API usage guide
- This file: Developer guidance
