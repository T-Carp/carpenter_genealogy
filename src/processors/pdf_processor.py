"""PDF processing for converting genealogy books to database format."""

import re
from pathlib import Path
from typing import List, Tuple, Optional
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..database.vector_store import VectorStore
from ..database.structured_store import StructuredStore
from ..database.models import ConfidenceLevel
from ..utils.config import Settings


class PDFProcessor:
    """Processes PDF documents for genealogy analysis."""

    def __init__(
        self,
        settings: Settings,
        vector_store: VectorStore,
        structured_store: StructuredStore,
    ):
        """Initialize PDF processor.

        Args:
            settings: Application settings
            vector_store: Vector database for narratives
            structured_store: Structured database for facts
        """
        self.settings = settings
        self.vector_store = vector_store
        self.structured_store = structured_store

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def extract_text_from_pdf(self, pdf_path: Path) -> List[Tuple[str, int]]:
        """Extract text from PDF with page numbers.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of (text, page_number) tuples
        """
        pages = []
        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            pages.append((text, page_num + 1))

        doc.close()
        return pages

    def chunk_text(
        self,
        pages: List[Tuple[str, int]],
        source_name: str,
    ) -> Tuple[List[str], List[dict]]:
        """Split text into chunks with metadata.

        Args:
            pages: List of (text, page_number) tuples
            source_name: Name of the source document

        Returns:
            Tuple of (chunks, metadata) lists
        """
        all_chunks = []
        all_metadata = []

        for text, page_num in pages:
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)

            for chunk in chunks:
                all_chunks.append(chunk)
                all_metadata.append({
                    "source": source_name,
                    "source_type": "book",
                    "page_number": page_num,
                })

        return all_chunks, all_metadata

    def extract_structured_data(self, text: str, page_num: int) -> List[dict]:
        """Extract structured genealogical data from text.

        This is a simplified implementation. In production, use:
        - NER models for entity extraction
        - Date parsing libraries
        - Relationship extraction models

        Args:
            text: Text to process
            page_num: Page number

        Returns:
            List of structured data entries
        """
        structured_data = []

        # Simple pattern matching for dates (e.g., "born 1850", "died 1920")
        birth_pattern = r"born\s+(?:in\s+)?(\d{4})"
        death_pattern = r"died\s+(?:in\s+)?(\d{4})"

        birth_matches = re.finditer(birth_pattern, text, re.IGNORECASE)
        death_matches = re.finditer(death_pattern, text, re.IGNORECASE)

        for match in birth_matches:
            structured_data.append({
                "type": "birth",
                "year": match.group(1),
                "page": page_num,
            })

        for match in death_matches:
            structured_data.append({
                "type": "death",
                "year": match.group(1),
                "page": page_num,
            })

        return structured_data

    def process_pdf(
        self,
        pdf_path: Path,
        source_name: Optional[str] = None,
    ) -> dict:
        """Process a PDF file and ingest into both databases.

        Args:
            pdf_path: Path to PDF file
            source_name: Optional name for the source (defaults to filename)

        Returns:
            Dictionary with processing statistics
        """
        if source_name is None:
            source_name = pdf_path.stem

        print(f"Processing PDF: {pdf_path}")

        # Extract text from PDF
        pages = self.extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(pages)} pages")

        # Chunk text for vector database
        chunks, metadata = self.chunk_text(pages, source_name)
        print(f"Created {len(chunks)} chunks")

        # Add to vector database
        chunk_ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]
        self.vector_store.add_documents(chunks, metadata, chunk_ids)
        print(f"Added {len(chunks)} chunks to vector database")

        # Extract structured data
        all_structured = []
        for text, page_num in pages:
            structured = self.extract_structured_data(text, page_num)
            all_structured.extend(structured)

        print(f"Extracted {len(all_structured)} structured data points")

        return {
            "source": source_name,
            "pages": len(pages),
            "chunks": len(chunks),
            "structured_items": len(all_structured),
        }

    def process_directory(self, directory: Path) -> List[dict]:
        """Process all PDFs in a directory.

        Args:
            directory: Directory containing PDF files

        Returns:
            List of processing results for each file
        """
        results = []

        pdf_files = list(directory.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files")

        for pdf_path in pdf_files:
            try:
                result = self.process_pdf(pdf_path)
                results.append(result)
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
                results.append({
                    "source": pdf_path.stem,
                    "error": str(e),
                })

        return results
