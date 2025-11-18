# FastAPI Learning Guide
*Using Your Genealogy API as Examples*

## Table of Contents
1. [What is an API?](#1-what-is-an-api)
2. [Understanding REST APIs](#2-understanding-rest-apis)
3. [HTTP Basics](#3-http-basics)
4. [FastAPI Fundamentals](#4-fastapi-fundamentals)
5. [Your API Structure](#5-your-api-structure)
6. [Path Operations (Routes)](#6-path-operations-routes)
7. [Request Parameters](#7-request-parameters)
8. [Response Models](#8-response-models)
9. [Dependency Injection](#9-dependency-injection)
10. [Error Handling](#10-error-handling)
11. [Testing Your API](#11-testing-your-api)
12. [Hands-On Exercises](#12-hands-on-exercises)

---

## 1. What is an API?

### The Simple Explanation

**API** = Application Programming Interface

Think of an API as a **waiter in a restaurant**:
- **You (Client)**: Order food from a menu
- **Waiter (API)**: Takes your order to the kitchen
- **Kitchen (Server/Database)**: Prepares your food
- **Waiter (API)**: Brings you the food

The waiter doesn't cook the food and you don't go into the kitchen. The waiter is the **interface** between you and the kitchen.

### In Your Genealogy App

Your FastAPI server is the "waiter" that:
- **Takes requests** from clients (web browser, mobile app, etc.)
- **Talks to your database** (SQLite with family data)
- **Returns formatted responses** (JSON data about people, relationships)

### Why Use an API?

```
Without API:
Web App → Directly accesses database (INSECURE, MESSY)

With API:
Web App → API Server → Database
Mobile App → API Server → Database
Python Script → API Server → Database
```

One API serves many clients safely!

---

## 2. Understanding REST APIs

### What is REST?

**REST** = Representational State Transfer

It's a set of rules for building APIs using standard HTTP methods.

### The 5 Core HTTP Methods (CRUD)

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Read/Retrieve data | Get person details |
| **POST** | Create new data | Add new person |
| **PUT** | Update existing data | Update person's info |
| **DELETE** | Delete data | Remove person |
| **PATCH** | Partial update | Update just birth year |

### RESTful URL Structure

```
Good REST API URLs:
GET    /api/genealogy/person/123        # Get person ID 123
POST   /api/genealogy/person            # Create new person
PUT    /api/genealogy/person/123        # Update person 123
DELETE /api/genealogy/person/123        # Delete person 123

Bad (non-RESTful):
GET /api/getPersonById?id=123
POST /api/createNewPerson
```

### In Your API

Look at `api.py` line 59-66 - your root endpoint lists all available endpoints:
```python
"endpoints": {
    "health": "/api/health",
    "search": "/api/genealogy/search?q=<query>",
    "surnames": "/api/genealogy/surnames",
    "person": "/api/genealogy/person/{id}",
    "graph": "/api/genealogy/graph",
}
```

Each endpoint follows REST principles!

---

## 3. HTTP Basics

### HTTP Request Structure

Every API request has these parts:

```http
GET /api/genealogy/person/5 HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer token123

[Optional Request Body]
```

1. **Method** (GET, POST, etc.)
2. **Path** (/api/genealogy/person/5)
3. **Headers** (metadata like content type)
4. **Body** (data for POST/PUT requests)

### HTTP Response Structure

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 5,
  "given_name": "John",
  "surname": "Carpenter",
  "birth_year": 1850
}
```

1. **Status Code** (200 = success, 404 = not found, etc.)
2. **Headers** (content type, etc.)
3. **Body** (the actual data)

### Common Status Codes

| Code | Meaning | When You'd Use It |
|------|---------|-------------------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST (created new person) |
| 400 | Bad Request | Invalid input data |
| 404 | Not Found | Person ID doesn't exist |
| 500 | Server Error | Database error, bug in code |

**In Your API**: See `routes.py` line 218 - raises 404 when person not found!

---

## 4. FastAPI Fundamentals

### Why FastAPI?

1. **Fast** - One of the fastest Python frameworks
2. **Easy** - Simple, intuitive syntax
3. **Automatic Docs** - Built-in Swagger UI
4. **Type Safety** - Uses Python type hints
5. **Modern** - Async support

### Your First FastAPI App

Let's break down `api.py`:

```python
# api.py line 21-28
app = FastAPI(
    title="Genealogy API",
    description="REST API for genealogy data",
    version="1.0.0",
    docs_url="/docs",      # 👈 Swagger UI location
    redoc_url="/redoc",    # 👈 Alternative docs
)
```

This creates your FastAPI application with automatic documentation!

### The Simplest Route

From `api.py` line 51-67:

```python
@app.get("/", tags=["root"])
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Genealogy API",
        "version": "1.0.0",
        "docs": "/docs"
    }
```

**Breaking it down:**
- `@app.get("/")` - Decorator that says "when someone visits `/`, run this function"
- `async def root()` - The function that handles the request
- `return {...}` - FastAPI automatically converts dict to JSON!

### Try It!

Start your API:
```bash
python api.py --port 8000
```

Visit in browser:
- http://localhost:8000/ - See the root response
- http://localhost:8000/docs - Interactive documentation!

---

## 5. Your API Structure

### File Organization

```
carpenter_genealogy/
├── api.py                        # Main application
└── src/api/
    ├── routes.py                 # All endpoint definitions
    └── dependencies.py           # Shared dependencies
```

### How They Connect

**api.py** (Main file):
```python
# Line 17: Import routes
from src.api.routes import router

# Line 48: Include them in the app
app.include_router(router)
```

**routes.py** (Endpoint definitions):
```python
# Line 101: Create a router
router = APIRouter(prefix="/api")

# Line 108: Define endpoints
@router.get("/health", response_model=HealthResponse)
async def health_check(...):
    ...
```

The `prefix="/api"` means all routes get `/api` prepended:
- `/health` becomes `/api/health`
- `/genealogy/search` becomes `/api/genealogy/search`

---

## 6. Path Operations (Routes)

### Basic GET Request

From `routes.py` line 108-132:

```python
@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check(
    store: StructuredStore = Depends(get_structured_store)
) -> HealthResponse:
    """Check API health and database connection."""
    try:
        # Test database connection
        session = store.Session()
        from ..database.structured_store import Person
        count = session.query(Person).count()
        session.close()

        return HealthResponse(
            status="healthy",
            database_connected=True
        )
    except Exception as e:
        return HealthResponse(
            status="degraded",
            database_connected=False
        )
```

**Key parts:**
1. `@router.get("/health")` - Listens for GET requests at `/api/health`
2. `response_model=HealthResponse` - Validates response matches model
3. `tags=["health"]` - Groups endpoints in docs
4. `async def health_check(...)` - The handler function
5. `return HealthResponse(...)` - Returns structured data

### GET with Path Parameter

From `routes.py` line 197-241:

```python
@router.get("/genealogy/person/{person_id}")
async def get_person(person_id: int, ...):
    """Get detailed information about a specific person."""
    # person_id is extracted from URL
    person = session.query(Person).filter(Person.id == person_id).first()

    if not person:
        raise HTTPException(status_code=404, detail=f"Person {person_id} not found")

    return PersonResponse(...)
```

**Using it:**
```bash
# Get person with ID 5
GET http://localhost:8000/api/genealogy/person/5

# FastAPI automatically extracts 5 and passes it to person_id
```

**The magic:** `{person_id}` in the path becomes a function parameter!

---

## 7. Request Parameters

### Three Types of Parameters

#### 1. Path Parameters (in URL)

```python
# routes.py line 197
@router.get("/genealogy/person/{person_id}")
async def get_person(person_id: int, ...):
    # person_id comes from URL: /person/123
```

#### 2. Query Parameters (after ?)

From `routes.py` line 139-180:

```python
@router.get("/genealogy/search")
async def search_people(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Result offset"),
    ...
):
```

**Using it:**
```bash
# URL with query parameters
GET /api/genealogy/search?q=John&limit=10&offset=0
```

**Query() options:**
- `...` = Required parameter
- `min_length=2` = Must be at least 2 characters
- `ge=1, le=100` = Greater or equal 1, less or equal 100
- `description` = Shows in API docs

#### 3. Request Body (for POST/PUT)

```python
@router.post("/genealogy/person")
async def create_person(
    person_data: PersonCreate,  # 👈 From request body
    ...
):
    # person_data comes from JSON in request body
```

### Query Parameters in Detail

From `routes.py` line 248-276:

```python
@router.get("/genealogy/graph")
async def get_family_graph(
    root_id: Optional[int] = Query(None, description="Root person ID"),
    generations: Optional[int] = Query(2, ge=1, le=10),
    include_ancestors: bool = Query(True),
    include_descendants: bool = Query(True),
    surname_filter: Optional[str] = Query(None),
    ...
):
```

**Understanding the types:**
- `Optional[int]` = Can be int or None (optional)
- `bool` = True/False
- `str` = Text

**Example usage:**
```bash
# Just root person
GET /api/genealogy/graph?root_id=5

# With multiple parameters
GET /api/genealogy/graph?root_id=5&generations=3&surname_filter=Carpenter

# With boolean
GET /api/genealogy/graph?include_ancestors=false
```

---

## 8. Response Models

### What are Response Models?

Response models define the **structure** of data your API returns. They:
1. **Validate** output matches expected format
2. **Document** what clients should expect
3. **Type-check** at development time

### Simple Response Model

From `routes.py` line 17-28:

```python
class PersonResponse(BaseModel):
    """Person data response model."""
    id: int
    given_name: Optional[str] = None
    surname: Optional[str] = None
    full_name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    birth_place: Optional[str] = None
    death_place: Optional[str] = None
    gender: Optional[str] = None
    maiden_name: Optional[str] = None
```

**Breaking it down:**
- `class PersonResponse(BaseModel)` - Inherits from Pydantic BaseModel
- `id: int` - Required integer field
- `given_name: Optional[str] = None` - Optional string field
- FastAPI automatically converts to JSON!

**What clients receive:**
```json
{
  "id": 5,
  "given_name": "John",
  "surname": "Carpenter",
  "full_name": "John Carpenter",
  "birth_year": 1850,
  "death_year": 1920,
  "birth_place": "Virginia",
  "death_place": "Texas",
  "gender": "M",
  "maiden_name": null
}
```

### Nested Response Models

From `routes.py` line 83-87:

```python
class GraphResponse(BaseModel):
    """Complete graph response."""
    nodes: List[GraphNodeResponse]      # List of nodes
    edges: List[GraphEdgeResponse]      # List of edges
    metadata: GraphMetadataResponse     # Single metadata object
```

This creates a **nested JSON structure**:
```json
{
  "nodes": [
    {"id": 1, "full_name": "John Carpenter", ...},
    {"id": 2, "full_name": "Mary Smith", ...}
  ],
  "edges": [
    {"source": 1, "target": 2, "relationship_type": "parent"}
  ],
  "metadata": {
    "total_nodes": 2,
    "total_edges": 1,
    "surnames": ["Carpenter", "Smith"]
  }
}
```

### Using Response Models

From `routes.py` line 197:

```python
@router.get("/genealogy/person/{person_id}", response_model=PersonResponse)
async def get_person(person_id: int, ...) -> PersonResponse:
    ...
    return PersonResponse(
        id=person.id,
        given_name=person.first_name,
        surname=person.last_name,
        full_name=full_name,
        ...
    )
```

The `response_model=PersonResponse` tells FastAPI:
1. Validate the return value matches PersonResponse
2. Show PersonResponse structure in docs
3. Filter out any extra fields not in model

---

## 9. Dependency Injection

### What is Dependency Injection?

Instead of creating database connections in every function, you **inject** them as parameters.

**Without DI (BAD):**
```python
async def get_person(person_id: int):
    settings = get_settings()           # Repeat in every function
    store = StructuredStore(settings)   # Repeat in every function
    session = store.Session()           # Repeat in every function
    # ... do work
```

**With DI (GOOD):**
```python
async def get_person(
    person_id: int,
    store: StructuredStore = Depends(get_structured_store)  # Injected!
):
    session = store.Session()
    # ... do work
```

### Your Dependencies

From `dependencies.py` line 23-34:

```python
def get_structured_store() -> Generator[StructuredStore, None, None]:
    """Get StructuredStore instance for dependency injection."""
    settings = get_api_settings()
    store = StructuredStore(settings)
    try:
        yield store
    finally:
        pass  # StructuredStore manages its own connections
```

**How it works:**
1. FastAPI sees `Depends(get_structured_store)`
2. Calls `get_structured_store()` once per request
3. Injects the result into your function
4. Runs cleanup code in `finally` block after request

### Using Dependencies

From `routes.py` line 197-200:

```python
@router.get("/genealogy/person/{person_id}")
async def get_person(
    person_id: int,
    store: StructuredStore = Depends(get_structured_store)  # 👈 Injected!
):
    session = store.Session()
    person = session.query(Person).filter(Person.id == person_id).first()
    # ... use store
```

### Why Use Dependencies?

1. **Code reuse** - Write connection logic once
2. **Easy testing** - Mock dependencies in tests
3. **Clean code** - Functions focus on logic, not setup
4. **Resource management** - Automatic cleanup

### Cached Dependencies

From `dependencies.py` line 13-20:

```python
@lru_cache()
def get_api_settings() -> Settings:
    """Get cached settings instance."""
    return get_settings()
```

The `@lru_cache()` decorator means:
- Settings loaded **once** when first needed
- Reused for all subsequent requests
- Faster and more efficient!

---

## 10. Error Handling

### HTTP Exceptions

From `routes.py` line 218:

```python
if not person:
    raise HTTPException(
        status_code=404,
        detail=f"Person {person_id} not found"
    )
```

**What happens:**
1. Exception raised
2. FastAPI catches it
3. Returns proper HTTP response:
```json
{
  "detail": "Person 5 not found"
}
```

### Status Codes

From `routes.py` line 179:

```python
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

Common patterns:
- **404** - Resource not found
- **400** - Bad request (invalid input)
- **500** - Server error (bugs, database issues)

### Try-Except Pattern

From `routes.py` line 242-245:

```python
try:
    # Your logic here
    person = session.query(Person).filter(...).first()
    if not person:
        raise HTTPException(status_code=404, ...)
    return PersonResponse(...)
except HTTPException:
    raise  # Re-raise HTTP exceptions as-is
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

**Pattern breakdown:**
1. Try to execute logic
2. If it's already an HTTPException (like 404), re-raise it
3. If it's any other error (database, bug), wrap in 500 error

---

## 11. Testing Your API

### Using Swagger UI (Built-in)

1. Start your API:
```bash
python api.py --port 8000
```

2. Open browser: http://localhost:8000/docs

3. You'll see interactive documentation:
   - Click an endpoint (e.g., `/api/health`)
   - Click "Try it out"
   - Click "Execute"
   - See the response!

### Using curl (Command Line)

```bash
# Health check
curl http://localhost:8000/api/health

# Search for person
curl "http://localhost:8000/api/genealogy/search?q=John&limit=5"

# Get specific person
curl http://localhost:8000/api/genealogy/person/5

# Get all surnames
curl http://localhost:8000/api/genealogy/surnames
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/health")
print(response.json())
# {'status': 'healthy', 'version': '1.0.0', 'database_connected': True}

# Search
response = requests.get(
    "http://localhost:8000/api/genealogy/search",
    params={"q": "John", "limit": 5}
)
print(response.json())

# Get person
response = requests.get("http://localhost:8000/api/genealogy/person/5")
if response.status_code == 200:
    person = response.json()
    print(f"Found: {person['full_name']}")
elif response.status_code == 404:
    print("Person not found")
```

### Testing with httpie (Pretty CLI tool)

```bash
# Install
pip install httpie

# Use it
http GET localhost:8000/api/health
http GET localhost:8000/api/genealogy/search q==John limit==5
http GET localhost:8000/api/genealogy/person/5
```

---

## 12. Hands-On Exercises

### Exercise 1: Make Your First Request

**Goal:** Successfully call the health endpoint

```bash
# Start your API
python api.py --port 8000

# In another terminal or browser, visit:
# http://localhost:8000/api/health
```

**Expected result:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database_connected": true
}
```

---

### Exercise 2: Search for People

**Goal:** Search your database for people with specific names

```bash
# Search for "Alexander"
curl "http://localhost:8000/api/genealogy/search?q=Alexander"

# Search with limit
curl "http://localhost:8000/api/genealogy/search?q=John&limit=3"

# Try in browser:
# http://localhost:8000/api/genealogy/search?q=Carpenter
```

**Questions to explore:**
- What happens if you search for ""? (Empty string - should fail due to min_length)
- What happens if you set limit=200? (Should fail, max is 100)
- Try searching for just "J" - what error do you get?

---

### Exercise 3: Get Person Details

**Goal:** Retrieve detailed info about a specific person

```bash
# Pick a person ID from your search results, then:
curl http://localhost:8000/api/genealogy/person/5

# Try a person that doesn't exist:
curl http://localhost:8000/api/genealogy/person/99999
```

**Expected:**
- Valid ID: Returns person details
- Invalid ID: 404 error with message "Person 99999 not found"

---

### Exercise 4: Explore the Family Graph

**Goal:** Get graph data for visualization

```bash
# Get full graph (might be large!)
curl http://localhost:8000/api/genealogy/graph

# Get graph starting from person 5, 3 generations
curl "http://localhost:8000/api/genealogy/graph?root_id=5&generations=3"

# Filter by surname
curl "http://localhost:8000/api/genealogy/graph?surname_filter=Carpenter"

# Only descendants (no ancestors)
curl "http://localhost:8000/api/genealogy/graph?root_id=5&include_ancestors=false"
```

**Observe:**
- How the `nodes` and `edges` arrays relate to each other
- How `metadata` provides summary information
- Try different combinations of parameters

---

### Exercise 5: Understand the Response

**Goal:** Parse JSON responses programmatically

Create a Python script:

```python
# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

def get_person_info(person_id):
    """Get and print person information."""
    response = requests.get(f"{BASE_URL}/api/genealogy/person/{person_id}")

    if response.status_code == 200:
        person = response.json()
        print(f"\nPerson {person_id}:")
        print(f"  Name: {person['full_name']}")
        print(f"  Birth Year: {person.get('birth_year', 'Unknown')}")
        print(f"  Death Year: {person.get('death_year', 'Unknown')}")
        print(f"  Birth Place: {person.get('birth_place', 'Unknown')}")
    else:
        print(f"\nError: {response.status_code}")
        print(f"  {response.json().get('detail', 'Unknown error')}")

def search_and_display(query):
    """Search and display results."""
    response = requests.get(
        f"{BASE_URL}/api/genealogy/search",
        params={"q": query, "limit": 5}
    )

    data = response.json()
    print(f"\nSearch results for '{query}':")
    print(f"Total found: {data['total']}")
    print("\nTop results:")
    for result in data['results']:
        print(f"  - {result['name']} (ID: {result['id']})")

# Try them
if __name__ == "__main__":
    search_and_display("Alexander")
    get_person_info(5)  # Try with a real ID from your database
```

Run it:
```bash
python test_api.py
```

---

### Exercise 6: Add a New Endpoint (Advanced)

**Goal:** Create your own endpoint to count people by surname

Add to `routes.py` around line 195 (before the person endpoint):

```python
@router.get("/genealogy/stats/by-surname", tags=["genealogy"])
async def get_surname_stats(
    store: StructuredStore = Depends(get_structured_store)
) -> Dict[str, int]:
    """Get count of people by surname.

    Returns:
        Dictionary mapping surname to count
    """
    try:
        session = store.Session()
        from ..database.structured_store import Person
        from sqlalchemy import func

        # Query: group by surname, count each
        results = session.query(
            Person.last_name,
            func.count(Person.id)
        ).group_by(Person.last_name).all()

        session.close()

        # Convert to dict
        stats = {surname: count for surname, count in results if surname}
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Test it:**
```bash
# Restart API
python api.py --reload

# Call your new endpoint
curl http://localhost:8000/api/genealogy/stats/by-surname

# Or visit in browser:
# http://localhost:8000/api/genealogy/stats/by-surname
```

**Expected result:**
```json
{
  "Carpenter": 45,
  "Smith": 12,
  "Johnson": 8,
  ...
}
```

---

### Exercise 7: Understanding CORS

**Goal:** Learn why CORS matters

From `api.py` line 30-45:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React
        "http://localhost:7860",  # Gradio
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**What is CORS?**
- Cross-Origin Resource Sharing
- Browser security feature
- Prevents malicious websites from accessing your API

**Try this:**
1. Create `test.html`:
```html
<!DOCTYPE html>
<html>
<body>
<h1>API Test</h1>
<button onclick="testAPI()">Call API</button>
<div id="result"></div>

<script>
async function testAPI() {
    const response = await fetch('http://localhost:8000/api/health');
    const data = await response.json();
    document.getElementById('result').innerText = JSON.stringify(data, null, 2);
}
</script>
</body>
</html>
```

2. Open `test.html` in browser
3. Click button - it works! (because CORS is configured)

4. Try removing localhost:3000 from `allow_origins` and restart API
5. Click button - **CORS error!** (browser blocks it)

This is why you need CORS configuration for web apps!

---

## Advanced Concepts

### Async vs Sync

You'll see both `async def` and regular `def`:

```python
# Async - can handle multiple requests concurrently
async def get_person(person_id: int):
    # Use 'await' for async operations
    result = await database.fetch_one()
    return result

# Sync - handles one request at a time
def get_person(person_id: int):
    # Regular function calls
    result = database.fetch_one()
    return result
```

**When to use async:**
- I/O operations (database, API calls, file reads)
- High-traffic APIs
- When you use `await` inside the function

**Your API uses async** even though most operations are sync - that's fine!

---

### Background Tasks

For operations that take time but user doesn't need to wait:

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email (takes time)
    time.sleep(5)
    print(f"Email sent to {email}")

@router.post("/notify")
async def notify_user(
    email: str,
    background_tasks: BackgroundTasks
):
    # Add task to background
    background_tasks.add_task(send_email, email, "Hello!")

    # Return immediately (don't wait for email)
    return {"message": "Notification queued"}
```

---

### Middleware

Middleware runs **before** and **after** every request.

**Example:** Logging middleware

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Before request
    print(f"Request: {request.method} {request.url}")

    # Process request
    response = await call_next(request)

    # After request
    print(f"Response: {response.status_code}")

    return response
```

**Your API uses CORS middleware** (line 32 in api.py)!

---

## Quick Reference

### Common FastAPI Decorators

```python
@router.get("/path")       # GET request
@router.post("/path")      # POST request (create)
@router.put("/path/{id}")  # PUT request (update)
@router.delete("/path/{id}") # DELETE request
@router.patch("/path/{id}") # PATCH request (partial update)
```

### Parameter Types

```python
# Path parameter
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    pass

# Query parameter
@router.get("/users")
async def list_users(
    limit: int = Query(10),
    offset: int = Query(0)
):
    pass

# Request body
@router.post("/users")
async def create_user(user: UserCreate):
    pass

# Dependency injection
@router.get("/users")
async def list_users(
    db: Session = Depends(get_db)
):
    pass
```

### Response Codes

```python
from fastapi import status

return JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={"message": "Created"}
)

# Or just return and let FastAPI handle it:
return {"message": "OK"}  # Automatically 200
```

---

## Next Steps

### 1. Read FastAPI Documentation
- Official docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### 2. Practice with Your API
- Try all the exercises above
- Add new endpoints
- Experiment with different parameters

### 3. Learn More About:
- **SQLAlchemy** - Your database ORM
- **Pydantic** - Data validation
- **Async Python** - Concurrent programming
- **Testing** - pytest with FastAPI

### 4. Build Features
Ideas for your genealogy API:
- Export family tree to GEDCOM format
- Upload photos for people
- Add timeline endpoint (chronological events)
- Create statistics endpoint (oldest person, etc.)
- Add authentication (login/logout)

---

## Troubleshooting

### API won't start
```bash
# Check if port is already in use
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
python api.py --port 8001
```

### Import errors
```bash
# Make sure you're in project root
cd /path/to/carpenter_genealogy

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database errors
```bash
# Check database exists
ls data/structured_db/genealogy.db

# If missing, run population scripts
cd parsers
python populate_alexander_lineage.py
```

### Can't access from browser
- Make sure API is running: `python api.py`
- Check the URL: `http://localhost:8000/docs`
- Try curl: `curl http://localhost:8000/api/health`

---

## Summary

You've learned:

✅ **What APIs are** and why they're useful
✅ **REST principles** for designing APIs
✅ **HTTP basics** (methods, status codes, requests/responses)
✅ **FastAPI fundamentals** (routes, decorators, async)
✅ **Path operations** (@router.get, @router.post, etc.)
✅ **Request parameters** (path, query, body)
✅ **Response models** (Pydantic BaseModel)
✅ **Dependency injection** (Depends())
✅ **Error handling** (HTTPException)
✅ **Testing** (Swagger UI, curl, Python requests)

**Your genealogy API is a real, production-quality API!** You can:
- Search people
- Get person details
- Retrieve family graphs
- Get relationships
- Check health status

Keep experimenting and building! 🚀
