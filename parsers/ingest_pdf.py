#!/usr/bin/env python3
"""Script to ingest PDF files into the genealogy database."""

import argparse
from pathlib import Path

from src.database.vector_store import VectorStore
from src.database.structured_store import StructuredStore
from src.processors.pdf_processor import PDFProcessor
from src.utils.config import get_settings


def main():
    """Ingest PDF files."""
    parser = argparse.ArgumentParser(
        description="Ingest PDF genealogy books into the database"
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to PDF file or directory containing PDFs",
    )
    parser.add_argument(
        "--source-name",
        type=str,
        help="Name for the source (defaults to filename)",
    )

    args = parser.parse_args()

    # Initialize components
    settings = get_settings()
    vector_store = VectorStore(settings)
    structured_store = StructuredStore(settings)
    processor = PDFProcessor(settings, vector_store, structured_store)

    # Process PDF(s)
    pdf_path = args.pdf_path

    if pdf_path.is_file():
        print(f"Processing single PDF: {pdf_path}")
        result = processor.process_pdf(pdf_path, args.source_name)
        print("\nResults:")
        print(f"  Source: {result['source']}")
        print(f"  Pages: {result['pages']}")
        print(f"  Chunks: {result['chunks']}")
        print(f"  Structured items: {result['structured_items']}")

    elif pdf_path.is_dir():
        print(f"Processing directory: {pdf_path}")
        results = processor.process_directory(pdf_path)
        print(f"\nProcessed {len(results)} files")

        for result in results:
            if "error" in result:
                print(f"  ❌ {result['source']}: {result['error']}")
            else:
                print(f"  ✓ {result['source']}: {result['chunks']} chunks")

    else:
        print(f"Error: {pdf_path} is not a valid file or directory")
        return

    print("\n✓ Ingestion complete!")


if __name__ == "__main__":
    main()
