# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Genealogy data management system for the Carpenter family. The system provides:
1. **Data Entry & Verification Tool** - Gradio-based interface for managing genealogy data
2. **RESTful API** - FastAPI endpoints for programmatic access to family data
3. **Family Tree Visualization** - D3.js-based interactive family tree visualization
4. **Data Parsing Scripts** - Tools for parsing and populating lineage data from various sources

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional, for custom settings)
cp .env.example .env
# Edit .env if needed
```

### Running the Applications

#### Data Entry Tool (Gradio)
```bash
# Start the Gradio data entry interface
python data_entry_tool.py

# Access at http://localhost:7860
```

#### API Server (FastAPI)
```bash
# Start the FastAPI server
python api.py

# Or with uvicorn directly
uvicorn api:app --reload --port 8000

# API docs available at:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Data Population Scripts
```bash
# Run lineage population scripts from parsers/ directory
cd parsers
python populate_alexander_lineage.py
python populate_john_lineage.py
python populate_richard_lineage.py
# ... etc for other lineages
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

The system uses a **simple, focused architecture**:

1. **Data Layer**: SQLite database with SQLAlchemy ORM
2. **API Layer**: FastAPI RESTful endpoints
3. **UI Layer**: Gradio data entry tool
4. **Visualization Layer**: D3.js family tree rendering

### Database Architecture

**SQLite with SQLAlchemy ORM** (`src/database/structured_store.py`):

**Schema**:
- `persons`:
  - id, given_name, middle_name, surname, maiden_name
  - birth_year, birth_place, death_year, death_place
  - generation, gender, confidence_level

- `relationships`:
  - id, person1_id, person2_id, relationship_type, confidence_level

- `partnerships`:
  - id, person1_id, person2_id, marriage_year, marriage_place, end_year, confidence_level

- `citations`:
  - id, source_type, source_name, page_number, section, url, notes

**Location**: `data/structured_db/genealogy.db`

### Data Models

**Pydantic Models** (`src/database/models.py`):

Core models that define the system's data structures:
- `Person`: Individual with biographical information
- `Relationship`: Parent-child, sibling, and other familial relationships
- `Partnership`: Marriage or long-term partnerships
- `Citation`: Source documentation for data provenance
- `ConfidenceLevel` (Enum): confirmed | likely | possible | uncertain

**Important**: All database operations use these models for type safety and validation.

### API Layer

**FastAPI Routes** (`src/api/routes.py`):

RESTful endpoints for:
- **Persons**: CRUD operations, search, filtering
- **Relationships**: Create, retrieve, query family connections
- **Partnerships**: Manage marriage/partnership records
- **Family Tree Data**: Get hierarchical tree structure for visualization
- **Statistics**: Database stats and metrics

**Key Features**:
- Automatic OpenAPI/Swagger documentation
- Pydantic validation
- Proper HTTP status codes
- Error handling with detailed messages

### UI Layer

**Gradio Data Entry Tool** (`data_entry_tool.py`):

Multi-tab interface:
1. **Person Management**: Add, edit, search people
2. **Relationship Management**: Define family connections
3. **Partnership Management**: Record marriages/partnerships
4. **Data Verification**: Review and validate entries
5. **Family Tree Visualization**: Interactive D3.js tree

**Key Features**:
- Real-time filtering and search
- Duplicate detection
- Data validation
- Export functionality

### Visualization Layer

**D3.js Family Tree** (`src/visualizations/`):

- **D3 Tidy Tree** (`d3_tidy_tree.py`): Generates hierarchical tree layout
- **Family Tree Viz** (`family_tree_viz.py`): Handles data transformation
- **Graph Builder** (`graph_builder.py`): Constructs family graph from database

**JavaScript** (`tidy_tree.js`): Client-side D3.js rendering

**Features**:
- Interactive exploration
- Collapsible nodes
- Generational levels
- Relationship indicators

### Data Parsing

**Lineage Population Scripts** (`parsers/`):

Scripts for importing data from various sources:
- `populate_alexander_lineage.py`
- `populate_john_lineage.py`
- `populate_richard_lineage.py`
- `populate_stephen_lineage.py`
- `populate_mary_lineage.py`
- `populate_berry_lineage.py`
- `populate_george_lineage.py`
- `populate_milly_lineage.py`
- `populate_susan_lineage.py`

These scripts parse structured data and populate the database with proper relationships.

## Common Development Tasks

### Adding New API Endpoints

1. Define Pydantic response model in `src/database/models.py`:
```python
class NewResponse(BaseModel):
    field: str
```

2. Add route in `src/api/routes.py`:
```python
@router.get("/new-endpoint", response_model=NewResponse)
async def get_something(store: StructuredStore = Depends(get_store)):
    # Implementation
    return NewResponse(field="value")
```

3. Test at http://localhost:8000/docs

### Adding New Database Fields

1. Update Pydantic model in `src/database/models.py`
2. Update SQLAlchemy model in `src/database/structured_store.py`
3. For existing databases, either:
   - Create migration script
   - Or drop/recreate for development: `rm data/structured_db/genealogy.db`

### Modifying Gradio Interface

Edit `data_entry_tool.py`:
- Add new tabs in the `create_gradio_interface()` function
- Add new event handlers for user interactions
- Update data display methods

### Adding New Visualization Features

1. Update data preparation in `src/visualizations/`
2. Modify D3.js rendering in `tidy_tree.js`
3. Update API endpoint if new data structure needed

## File Structure

```
carpenter_genealogy/
├── api.py                      # FastAPI application entry point
├── data_entry_tool.py          # Gradio UI application
├── tidy_tree.js                # D3.js visualization
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration (not in git)
├── data/
│   ├── structured_db/          # SQLite database
│   └── exports/                # Exported data files
├── parsers/                    # Data parsing scripts
│   ├── populate_*.py           # Lineage population scripts
│   └── parse_*.py              # Data parsing utilities
└── src/
    ├── api/
    │   ├── routes.py           # FastAPI routes
    │   └── dependencies.py     # Dependency injection
    ├── database/
    │   ├── models.py           # Pydantic data models
    │   └── structured_store.py # SQLAlchemy ORM & database
    ├── ui/
    │   └── family_tree_tab.py  # Family tree visualization tab
    ├── utils/
    │   └── config.py           # Configuration management
    └── visualizations/
        ├── d3_tidy_tree.py     # D3 tree layout generation
        ├── family_tree_viz.py  # Tree data transformation
        └── graph_builder.py    # Graph construction
```

## Data Model Relationships

```
Person
  ├─→ Relationships (as person1 or person2)
  │   └─→ Person (related person)
  ├─→ Partnerships (as person1 or person2)
  │   └─→ Person (partner)
  └─→ Citations (optional)

Relationship
  ├─→ Person (person1)
  ├─→ Person (person2)
  └─→ Citation (optional)

Partnership
  ├─→ Person (person1)
  ├─→ Person (person2)
  └─→ Citation (optional)
```

## API Endpoints Reference

### Persons
- `GET /persons/` - List all persons with optional filters
- `GET /persons/{person_id}` - Get specific person details
- `POST /persons/` - Create new person
- `PUT /persons/{person_id}` - Update person
- `DELETE /persons/{person_id}` - Delete person
- `GET /persons/search/` - Search persons by name

### Relationships
- `GET /relationships/` - List all relationships
- `GET /relationships/{relationship_id}` - Get specific relationship
- `POST /relationships/` - Create new relationship
- `GET /relationships/person/{person_id}` - Get person's relationships

### Partnerships
- `GET /partnerships/` - List all partnerships
- `POST /partnerships/` - Create new partnership
- `GET /partnerships/person/{person_id}` - Get person's partnerships

### Visualization
- `GET /family-tree/{root_person_id}` - Get hierarchical tree data
- `GET /family-tree/descendants/{person_id}` - Get descendants tree
- `GET /family-tree/ancestors/{person_id}` - Get ancestors tree

### Statistics
- `GET /stats/` - Get database statistics

## Environment Variables

Create a `.env` file (optional):

```bash
# Database
STRUCTURED_DB_PATH=./data/structured_db/genealogy.db

# API
API_HOST=0.0.0.0
API_PORT=8000

# Application
APP_TITLE=Carpenter Family Genealogy
APP_DESCRIPTION=Family genealogy data management and visualization
```

## Future Enhancement Areas

1. **Authentication & Authorization**: Add user login and permissions
2. **Advanced Search**: Full-text search across all fields
3. **Photo/Document Upload**: Attach images and documents to persons
4. **Timeline View**: Chronological view of family events
5. **Export Features**: GEDCOM export for compatibility with other tools
6. **Mobile App**: React Native or Flutter mobile interface
7. **Collaborative Editing**: Multi-user editing with conflict resolution
8. **DNA Integration**: Import and visualize DNA test results

## Troubleshooting

### Database Issues
```bash
# Reset database (development only)
rm data/structured_db/genealogy.db

# Re-populate from parsers
cd parsers
python populate_alexander_lineage.py
# ... run other population scripts
```

### API Issues
```bash
# Check if port is in use
lsof -i :8000

# Run with different port
uvicorn api:app --port 8080
```

### Gradio Issues
```bash
# Check Gradio version
pip show gradio

# Reinstall if needed
pip install --upgrade gradio
```

### Import Errors
```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Testing

Currently no automated tests are implemented. To manually test:

1. **Data Entry Tool**: Run `python data_entry_tool.py` and test CRUD operations
2. **API**: Use Swagger UI at http://localhost:8000/docs to test endpoints
3. **Visualization**: Load family tree tab and verify rendering

Future: Add pytest-based test suite for API and database operations.

## Contributing

When adding new features:
1. Follow existing code structure
2. Use type hints (Pydantic models)
3. Update this CLAUDE.md file
4. Test both API and UI interfaces
5. Ensure data integrity in database operations
