#!/usr/bin/env python3
"""Check which Claude models are available with the API key."""

import os
from anthropic import Anthropic

# Load API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    # Try loading from .env file
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("Error: ANTHROPIC_API_KEY not found")
    exit(1)

client = Anthropic(api_key=api_key)

# Known Claude models to test
models_to_test = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-haiku-20241022",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-2.1",
    "claude-2.0",
]

print("Testing available Claude models with your API key...\n")
print("=" * 60)

available_models = []
unavailable_models = []

for model in models_to_test:
    try:
        # Try to make a minimal API call
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        available_models.append(model)
        print(f"✓ {model:40} AVAILABLE")
    except Exception as e:
        error_str = str(e)
        if "not_found_error" in error_str or "404" in error_str:
            unavailable_models.append(model)
            print(f"✗ {model:40} NOT AVAILABLE")
        else:
            print(f"? {model:40} ERROR: {str(e)[:50]}")

print("\n" + "=" * 60)
print(f"\nSummary:")
print(f"Available models: {len(available_models)}")
print(f"Unavailable models: {len(unavailable_models)}")

if available_models:
    print(f"\n✓ RECOMMENDED MODEL TO USE:")
    print(f"  {available_models[0]}")
