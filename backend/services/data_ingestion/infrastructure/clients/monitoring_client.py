import requests
from data_ingestion.core.config import MONITORING_BASE

class MonitoringClient:
    """
    Pushes livestatus snapshot.
    """

    def push_livestatus(self, event):
        url = f"{MONITORING_BASE}/api/v1/livestatus/"
        payload = {
            "device_id": str(event.device_id),
            "livestock_id": str(event.livestock_id),
            "metric": event.metric,
            "value": event.value,
            "recorded_at": event.recorded_at.isoformat(),
        }
        r = requests.post(url, json=payload, timeout=3)
        r.raise_for_status()
