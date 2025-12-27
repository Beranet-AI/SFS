from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class RuleDecision:
    violated: bool
    code: str
    details: dict


class RuleEvaluatorService:
    """
    Minimal "AI-ready" rule engine hook point.
    - Today: simple threshold / time-window rules
    - Tomorrow: AI hook can suggest thresholds or detect anomalies
    """

    def __init__(self, ai_hook: Optional[Callable[[dict], dict]] = None) -> None:
        self.ai_hook = ai_hook

    def evaluate(self, event: dict) -> list[RuleDecision]:
        decisions: list[RuleDecision] = []

        # Example threshold rule
        metric = event.get("metric")
        value = event.get("value")

        if metric == "temp" and isinstance(value, (int, float)) and value >= 45:
            decisions.append(
                RuleDecision(
                    violated=True,
                    code="TEMP_TOO_HIGH",
                    details={"metric": metric, "value": value},
                )
            )

        # Optional AI hook (future)
        if self.ai_hook:
            try:
                _ = self.ai_hook(event)
            except Exception:
                pass

        return decisions
