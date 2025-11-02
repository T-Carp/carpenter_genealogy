"""LLM wrapper with token tracking."""

from typing import Any, Dict, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage


class TrackedChatAnthropic(ChatAnthropic):
    """ChatAnthropic wrapper that tracks token usage."""

    def __init__(self, *args, step_name: str = "unknown", **kwargs):
        """Initialize with step name for tracking.

        Args:
            step_name: Name of the step using this LLM
            *args: Arguments for ChatAnthropic
            **kwargs: Keyword arguments for ChatAnthropic
        """
        super().__init__(*args, **kwargs)
        self.step_name = step_name
        self.last_usage: Optional[Dict[str, int]] = None

    def _generate(self, *args, **kwargs) -> Any:
        """Generate with token tracking."""
        result = super()._generate(*args, **kwargs)

        # Extract token usage from response
        if hasattr(result, "llm_output") and result.llm_output:
            usage = result.llm_output.get("usage", {})
            if usage:
                self.last_usage = {
                    "input_tokens": usage.get("input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                    "step_name": self.step_name,
                }

        return result

    async def _agenerate(self, *args, **kwargs) -> Any:
        """Async generate with token tracking."""
        result = await super()._agenerate(*args, **kwargs)

        # Extract token usage from response
        if hasattr(result, "llm_output") and result.llm_output:
            usage = result.llm_output.get("usage", {})
            if usage:
                self.last_usage = {
                    "input_tokens": usage.get("input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                    "step_name": self.step_name,
                }

        return result

    def get_last_usage(self) -> Optional[Dict[str, int]]:
        """Get usage from last API call.

        Returns:
            Dictionary with input_tokens, output_tokens, and step_name
        """
        return self.last_usage

    def reset_usage(self) -> None:
        """Reset usage tracking."""
        self.last_usage = None
