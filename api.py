"""FastAPI backend server for genealogy application.

This provides REST API endpoints for:
- Family graph data
- Person search
- Person details
- Relationships

Run with: python api.py --port 8000
"""

import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.api.routes import router
from src.utils.config import get_settings


# Create FastAPI app
app = FastAPI(
    title="Genealogy API",
    description="REST API for genealogy data and family tree visualization",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# Configure CORS - Allow all origins for development
# In production, replace with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (including file:// protocol)
    allow_credentials=False,  # Must be False when allow_origins is "*"
    allow_methods=["*"],  # GET, POST, etc.
    allow_headers=["*"],  # Accept all headers
)

# Include API routes
app.include_router(router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Genealogy API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/api/health",
            "search": "/api/genealogy/search?q=<query>",
            "surnames": "/api/genealogy/surnames",
            "person": "/api/genealogy/person/{id}",
            "graph": "/api/genealogy/graph",
            "relationships": "/api/genealogy/relationships/{id}",
        }
    }


@app.on_event("startup")
async def startup_event():
    """Run on API startup."""
    settings = get_settings()
    print("=" * 60)
    print("Genealogy API Starting")
    print("=" * 60)
    print(f"OpenAPI docs: http://localhost:8000/docs")
    print(f"ReDoc docs: http://localhost:8000/redoc")
    print(f"Database: {settings.structured_db_path}")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on API shutdown."""
    print("Genealogy API shutting down...")


def main():
    """Run the API server."""
    parser = argparse.ArgumentParser(description="Genealogy API Server")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run on (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes"
    )

    args = parser.parse_args()

    # Run server
    uvicorn.run(
        "api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
