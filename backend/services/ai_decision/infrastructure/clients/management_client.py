import requests
from ai_decision.core.config import MANAGEMENT_BASE

class ManagementClient:
    """
    Pushes predictions & incidents to Django management.
    """

    def push_health_prediction(self, prediction):
        url = f"{MANAGEMENT_BASE}/api/v1/livestock/{prediction.livestock_id}/evaluate-health/"
        payload = {
            "score": prediction.score,
        }
        r = requests.post(url, json=payload, timeout=3)
        r.raise_for_status()

    def create_incident(self, livestock_id: str, state, score: float):
        payload = {
            "livestock_id": livestock_id,
            "severity": "critical",
            "source": "ai",
            "description": f"AI predicted {state.value} (score={score})",
        }
        r = requests.post(
            f"{MANAGEMENT_BASE}/api/v1/incidents/",
            json=payload,
            timeout=3,
        )
        r.raise_for_status()
