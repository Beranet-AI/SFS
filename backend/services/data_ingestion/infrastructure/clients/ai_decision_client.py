import requests
from typing import Dict, Any
from backend.services.data_ingestion.core.config import settings

class AIDecisionClient:
    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # placeholder
        url = f"{settings.AI_DECISION_BASE_URL}/ai/evaluate"
        r = requests.post(url, json=payload, timeout=5)
        if r.status_code == 404:
            return {"actions": []}
        r.raise_for_status()
        return r.json()
