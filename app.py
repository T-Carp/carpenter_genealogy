#!/usr/bin/env python3
"""Main entry point for the Carpenter Genealogy Assistant."""

import argparse
from src.ui.gradio_app import launch_app


def main():
    """Run the application."""
    parser = argparse.ArgumentParser(
        description="Carpenter Family Genealogy Assistant"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public share link",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to run the server on (default: 7860)",
    )

    args = parser.parse_args()

    print("Starting Carpenter Genealogy Assistant...")
    print(f"Server will be available at http://localhost:{args.port}")

    launch_app(share=args.share, server_port=args.port)


if __name__ == "__main__":
    main()
