# Token Usage Tracking Guide

This guide shows you how to monitor token usage and costs for your genealogy assistant.

## Quick Monitoring (Estimates)

For quick estimates, use the monitoring script:

```bash
source venv/bin/activate
python monitor_tokens.py
```

This shows estimated token usage for each workflow step.

## Exact Tracking with LangSmith (Recommended)

For accurate, real-time token tracking, use LangSmith:

### 1. Sign Up for LangSmith

1. Go to https://smith.langchain.com/
2. Sign up for a free account
3. Get your API key from Settings → API Keys

### 2. Configure Your Environment

Add to your `.env` file:

```env
# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=genealogy-assistant
```

### 3. Run Your App

```bash
source venv/bin/activate
python app.py
```

### 4. View Detailed Traces

Visit https://smith.langchain.com/ and select your project to see:

- ✅ Exact token counts for each LLM call
- ✅ Latency for each step
- ✅ Full conversation history
- ✅ Cost breakdown by model
- ✅ Input/output for each step
- ✅ Error tracking

## Understanding Token Usage

### Current Workflow Steps That Use Tokens

1. **Query Router** (~500-800 input, ~100 output)
   - Analyzes query type
   - Cost: ~$0.003 per query

2. **Fact Extractor** (~800-1500 input, ~200 output)
   - Only runs for factual queries
   - Cost: ~$0.006 per query

3. **Synthesizer** (~2000-4000 input, ~400-800 output)
   - Main response generation
   - Largest token user
   - Cost: ~$0.015-0.025 per query

4. **Confidence Checker** (~800-1200 input, ~50 output)
   - Assesses reliability
   - Cost: ~$0.004 per query

### Total Per Query

**Typical Query:**
- Input tokens: 4,000-7,000
- Output tokens: 750-1,150
- **Total cost: $0.025-0.040 per query**

**Factual queries** (with fact extraction):
- Slightly higher: ~$0.030-0.045

**Exploratory queries** (longer responses):
- Can be higher: ~$0.035-0.050

## Cost Optimization Tips

### 1. Reduce Context Chunks

In `.env`, reduce the number of chunks retrieved:

```env
# Default: 20 chunks
MAX_CONTEXT_CHUNKS=15  # Saves ~20% tokens
```

### 2. Use Smaller Chunk Size

```env
# Default: 1500
CHUNK_SIZE=1000  # Reduces context size
```

### 3. Switch to Haiku for Testing

When developing/testing, use the cheaper model:

```env
CLAUDE_MODEL=claude-3-haiku-20240307  # ~80% cheaper
```

**Cost comparison per query:**
- Sonnet 4.5: $0.025-0.040
- Haiku: $0.004-0.008

### 4. Cache Common Queries

Implement caching for repeated questions:

```python
# In src/ui/gradio_app.py
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query_hash):
    return workflow.run(query)
```

## Manual Token Counting

If you want to manually count tokens without LangSmith:

```python
from anthropic import Anthropic

client = Anthropic()

# Count tokens in your prompt
message = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "your query here"}]
)

print(f"Input tokens: {message.input_tokens}")
```

## Monitoring Script Features

The `monitor_tokens.py` script provides:

1. **Interactive CLI** - Ask questions and see token estimates
2. **Step-by-step breakdown** - See which steps use most tokens
3. **Cost estimates** - Approximate cost per query
4. **Model information** - Current model and settings

```bash
python monitor_tokens.py

🔍 Enter your genealogy question: Tell me about the Keenum family

PROCESSING: Tell me about the Keenum family
======================================================================

📄 RESPONSE:
----------------------------------------------------------------------
[Your response here]
----------------------------------------------------------------------

💰 ESTIMATED TOKEN USAGE:
----------------------------------------------------------------------
Step                 Input (est.)     Output (est.)    Cost (est.)
----------------------------------------------------------------------
Query Routing        500              100              $0.0030
Fact Extraction      800              200              $0.0054
Synthesis            3,000            500              $0.0165
Confidence Check     800              50               $0.0031
----------------------------------------------------------------------
TOTAL (estimated)    5,100            850              $0.0280
```

## Budget Monitoring

### Set Up Budget Alerts

In Anthropic Console (https://console.anthropic.com/):
1. Go to Settings → Billing
2. Set spending limit
3. Configure email alerts
4. Monitor usage dashboard

### Track Monthly Spending

Assuming:
- 100 queries/day
- $0.03 average per query
- **Monthly cost: ~$90**

Adjust usage based on your budget:
- 50 queries/day = ~$45/month
- 25 queries/day = ~$22.50/month

## Troubleshooting

### LangSmith not showing traces

1. Check `.env` has correct API key
2. Verify `LANGCHAIN_TRACING_V2=true`
3. Restart your app after adding keys
4. Check network connectivity

### Token counts seem high

1. Check `MAX_CONTEXT_CHUNKS` - lower it if needed
2. Review chunk size settings
3. Consider using Haiku for non-critical queries
4. Implement query caching

### Want more detailed tracking

Use LangChain callbacks:

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = workflow.run(query)
    print(f"Tokens: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost}")
```

## Resources

- **LangSmith Docs**: https://docs.smith.langchain.com/
- **Anthropic Pricing**: https://www.anthropic.com/pricing
- **Token Counting**: https://docs.anthropic.com/claude/docs/token-counting
- **Usage Dashboard**: https://console.anthropic.com/settings/usage
