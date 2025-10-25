"""Token usage tracking for monitoring costs."""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TokenUsage:
    """Track token usage for a single operation."""

    step_name: str
    input_tokens: int = 0
    output_tokens: int = 0
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def total_tokens(self) -> int:
        """Total tokens used."""
        return self.input_tokens + self.output_tokens

    def get_cost(self, model: str = "claude-sonnet-4-5-20250929") -> float:
        """Calculate cost based on model pricing.

        Args:
            model: Model identifier

        Returns:
            Cost in USD
        """
        # Pricing per million tokens (as of 2024)
        pricing = {
            "claude-sonnet-4-5-20250929": {"input": 3.0, "output": 15.0},
            "claude-3-5-sonnet-20240620": {"input": 3.0, "output": 15.0},
            "claude-3-opus-20240229": {"input": 15.0, "output": 75.0},
            "claude-3-sonnet-20240229": {"input": 3.0, "output": 15.0},
            "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        }

        if model not in pricing:
            # Default to Sonnet pricing
            model = "claude-3-5-sonnet-20240620"

        input_cost = (self.input_tokens / 1_000_000) * pricing[model]["input"]
        output_cost = (self.output_tokens / 1_000_000) * pricing[model]["output"]

        return input_cost + output_cost


class TokenTracker:
    """Track token usage across workflow steps."""

    def __init__(self):
        """Initialize tracker."""
        self.usages: List[TokenUsage] = []
        self.current_query: str = ""

    def add_usage(
        self,
        step_name: str,
        input_tokens: int,
        output_tokens: int,
    ) -> None:
        """Add token usage for a step.

        Args:
            step_name: Name of the workflow step
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        """
        usage = TokenUsage(
            step_name=step_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
        self.usages.append(usage)

    def get_total_usage(self) -> Dict[str, int]:
        """Get total token usage.

        Returns:
            Dictionary with total input/output/total tokens
        """
        total_input = sum(u.input_tokens for u in self.usages)
        total_output = sum(u.output_tokens for u in self.usages)

        return {
            "input_tokens": total_input,
            "output_tokens": total_output,
            "total_tokens": total_input + total_output,
        }

    def get_total_cost(self, model: str) -> float:
        """Get total cost for all steps.

        Args:
            model: Model identifier

        Returns:
            Total cost in USD
        """
        return sum(u.get_cost(model) for u in self.usages)

    def get_report(self, model: str) -> str:
        """Generate a formatted usage report.

        Args:
            model: Model identifier

        Returns:
            Formatted report string
        """
        if not self.usages:
            return "No token usage recorded."

        lines = ["", "=" * 70, "TOKEN USAGE REPORT", "=" * 70, ""]

        # Per-step breakdown
        lines.append(f"{'Step':<25} {'Input':<12} {'Output':<12} {'Total':<12} {'Cost':<10}")
        lines.append("-" * 70)

        for usage in self.usages:
            cost = usage.get_cost(model)
            lines.append(
                f"{usage.step_name:<25} "
                f"{usage.input_tokens:<12,} "
                f"{usage.output_tokens:<12,} "
                f"{usage.total_tokens:<12,} "
                f"${cost:<9.4f}"
            )

        # Totals
        lines.append("-" * 70)
        totals = self.get_total_usage()
        total_cost = self.get_total_cost(model)

        lines.append(
            f"{'TOTAL':<25} "
            f"{totals['input_tokens']:<12,} "
            f"{totals['output_tokens']:<12,} "
            f"{totals['total_tokens']:<12,} "
            f"${total_cost:<9.4f}"
        )

        lines.append("=" * 70)
        lines.append("")

        return "\n".join(lines)

    def reset(self) -> None:
        """Reset tracker for new query."""
        self.usages = []
        self.current_query = ""
