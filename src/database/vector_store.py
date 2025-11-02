"""Vector database interface for narrative genealogy content."""

from pathlib import Path
from typing import List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from ..utils.config import Settings


class VectorStore:
    """Interface for vector database operations."""

    def __init__(self, settings: Settings):
        """Initialize vector store.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        # Initialize ChromaDB
        self.settings.vector_db_path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(self.settings.vector_db_path),
            settings=ChromaSettings(anonymized_telemetry=False),
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.settings.vector_db_collection,
            metadata={"description": "Genealogy narrative content"},
        )

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
        """Add documents to the vector store.

        Args:
            documents: List of text documents to add
            metadatas: Optional metadata for each document
            ids: Optional IDs for each document
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        if metadatas is None:
            metadatas = [{} for _ in documents]

        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()

        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )

    def search(
        self,
        query: str,
        n_results: int = 10,
        where: Optional[dict] = None,
    ) -> dict:
        """Search for relevant documents.

        Args:
            query: Search query
            n_results: Number of results to return
            where: Optional metadata filter

        Returns:
            Dictionary with search results
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()

        # Search collection
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=where,
        )

        return results

    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.client.delete_collection(name=self.settings.vector_db_collection)

    def get_stats(self) -> dict:
        """Get statistics about the vector store.

        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        return {
            "collection_name": self.settings.vector_db_collection,
            "document_count": count,
            "embedding_model": "all-MiniLM-L6-v2",
        }
