import requests
from monitoring.core.config import TELEMETRY_SERVICE_BASE

class TelemetryClient:
    """
    Pulls telemetry data from data_ingestion service.
    """

    def fetch_recent(self, livestock_id: str):
        url = f"{TELEMETRY_SERVICE_BASE}/api/v1/telemetry/recent/{livestock_id}/"
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        return r.json()
