from typing import Dict, Any
from data_ingestion.core.config import settings
import requests


class RuleDispatcher:
    """
    AI-ready: today it can call ai_decision; tomorrow AI can fetch rules/policies.
    """
    def dispatch(self, telemetry: Dict[str, Any]) -> None:
        if not settings.ENABLE_RULE_DISPATCH:
            return

        # placeholder endpoint (later implement in ai_decision)
        url = f"{settings.AI_DECISION_BASE_URL}/rules/evaluate"
        try:
            requests.post(url, json=telemetry, timeout=2)
        except Exception:
            # don't crash ingestion pipeline
            pass
