import requests
from backend.services.data_ingestion.core.config import RULES_BASE

class RulesClient:
    """
    Calls rules evaluation endpoint.
    """

    def evaluate(self, event):
        payload = {
            "livestock_id": str(event.livestock_id),
            "metric": event.metric,
            "value": event.value,
        }
        r = requests.post(f"{RULES_BASE}/evaluate/", json=payload, timeout=3)
        r.raise_for_status()
