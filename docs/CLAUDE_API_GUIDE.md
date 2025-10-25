# Claude API Guide for Genealogy Assistant

This guide explains how the Carpenter Genealogy Assistant uses the Claude API and how to configure it.

## Getting Started with Claude API

### 1. Obtain an API Key

1. Visit the [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** in the sidebar
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-`)
6. Store it securely - you won't be able to see it again

### 2. Configure Your Environment

Add your API key to the `.env` file:

```env
ANTHROPIC_API_KEY=sk-ant-api03-xxx-your-key-here-xxx
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## Claude Models

### Available Models

**Claude 3.5 Sonnet (Recommended)**
- Model ID: `claude-3-5-sonnet-20241022`
- Best balance of intelligence, speed, and cost
- Excellent for genealogy analysis
- Strong reasoning and citation capabilities

**Claude 3 Opus**
- Model ID: `claude-3-opus-20240229`
- Highest intelligence
- Best for complex family relationships
- Higher cost

**Claude 3 Haiku**
- Model ID: `claude-3-haiku-20240307`
- Fastest, most economical
- Good for simple fact extraction
- Lower accuracy on complex queries

### Changing Models

Edit `.env`:

```env
CLAUDE_MODEL=claude-3-opus-20240229
```

Or set environment variable:

```bash
export CLAUDE_MODEL=claude-3-opus-20240229
python app.py
```

## How the System Uses Claude

The genealogy assistant makes multiple API calls for each user query:

### 1. Query Routing
```python
# Analyzes query type and intent
llm = ChatAnthropic(model=settings.claude_model)
intent = llm.invoke("Analyze this genealogy query...")
```

**Purpose:** Determines if query is factual, exploratory, relationship-based, or timeline-based

**Tokens:** ~100-200 per query

### 2. Fact Extraction
```python
# Extracts structured facts from documents
facts = llm.invoke("Extract genealogical facts from...")
```

**Purpose:** Pulls specific dates, places, events from retrieved content

**Tokens:** ~500-1000 per query (depending on document length)

### 3. Response Synthesis
```python
# Creates narrative response
response = llm.invoke("Synthesize information about...")
```

**Purpose:** Generates comprehensive, contextualized answer

**Tokens:** ~1000-2000 per query (depending on context length)

### 4. Confidence Assessment
```python
# Evaluates information reliability
confidence = llm.invoke("Assess confidence level...")
```

**Purpose:** Determines how certain we can be about the information

**Tokens:** ~300-500 per query

### Total Usage Per Query

**Typical Query:**
- Input tokens: ~2000-4000
- Output tokens: ~500-1000
- Total: ~2500-5000 tokens

**Cost Estimate (Claude 3.5 Sonnet):**
- Input: $3 per million tokens
- Output: $15 per million tokens
- Per query: ~$0.01-0.02

## API Configuration Options

### In `src/utils/config.py`:

```python
class Settings(BaseSettings):
    # Claude API
    anthropic_api_key: str
    claude_model: str = "claude-3-5-sonnet-20241022"

    # Generation parameters (can be added)
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
```

### Custom Parameters

Modify agent initialization in `src/agents/`:

```python
self.llm = ChatAnthropic(
    model=settings.claude_model,
    api_key=settings.anthropic_api_key,
    temperature=0.7,  # Lower = more deterministic
    max_tokens=4096,   # Maximum response length
)
```

## Best Practices

### 1. API Key Security

**DO:**
- Store API key in `.env` file (not committed to git)
- Use environment variables in production
- Rotate keys periodically
- Use separate keys for dev/prod

**DON'T:**
- Hardcode API keys in source code
- Commit `.env` file to version control
- Share API keys in public repositories
- Use personal keys in shared environments

### 2. Cost Optimization

**Reduce Costs:**
```python
# Limit context chunks
MAX_CONTEXT_CHUNKS=5  # Instead of 10

# Use smaller model for simple queries
if query_type == QueryType.FACTUAL:
    model = "claude-3-haiku-20240307"
else:
    model = "claude-3-5-sonnet-20241022"
```

**Implement Caching:**
```python
# Cache common queries
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(query_hash):
    return workflow.run(query)
```

### 3. Rate Limiting

Claude API has rate limits. Implement retry logic:

```python
from anthropic import RateLimitError
import time

def call_with_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if i < max_retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
            else:
                raise
```

### 4. Error Handling

```python
from anthropic import APIError, APIConnectionError

try:
    response = llm.invoke(prompt)
except APIConnectionError:
    # Network issue
    return "Connection error. Please try again."
except APIError as e:
    # API error
    return f"API error: {e.message}"
```

## Monitoring Usage

### 1. Anthropic Console

Visit https://console.anthropic.com/settings/usage to:
- View usage statistics
- Set spending limits
- Download usage reports
- Track costs by project

### 2. Programmatic Tracking

Add logging to track API calls:

```python
import logging

logger = logging.getLogger(__name__)

def log_api_call(query, tokens_used):
    logger.info(f"API call for query: {query[:50]}...")
    logger.info(f"Tokens used: {tokens_used}")
```

### 3. Budget Alerts

Set up budget alerts in the Anthropic Console:
1. Go to Settings → Usage
2. Click "Set spending limit"
3. Configure email alerts

## Advanced: Streaming Responses

For real-time responses in the UI:

```python
async def stream_response(query):
    async with ChatAnthropic(
        model=settings.claude_model,
        streaming=True,
    ) as llm:
        async for chunk in llm.astream(prompt):
            yield chunk.content
```

Update Gradio UI:

```python
def chat_stream(message, history):
    response = ""
    for chunk in stream_response(message):
        response += chunk
        yield history + [(message, response)]
```

## Troubleshooting

### Invalid API Key
```
Error: Invalid API key
```

**Solution:** Check that your API key is correct in `.env` file

### Rate Limit Exceeded
```
Error: Rate limit exceeded
```

**Solution:** Implement retry logic with exponential backoff

### Context Length Exceeded
```
Error: Prompt is too long
```

**Solution:** Reduce `MAX_CONTEXT_CHUNKS` or `CHUNK_SIZE` in settings

### Model Not Found
```
Error: Model not found
```

**Solution:** Verify model ID is correct and you have access to it

## Support

- **API Documentation:** https://docs.anthropic.com/
- **API Status:** https://status.anthropic.com/
- **Support:** support@anthropic.com
- **Discord:** https://discord.gg/anthropic
