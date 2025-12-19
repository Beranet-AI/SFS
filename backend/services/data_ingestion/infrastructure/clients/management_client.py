import requests
from data_ingestion.core.config import MANAGEMENT_BASE

class ManagementClient:
    """
    Pushes telemetry into Django management service.
    """

    def push_telemetry(self, event):
        url = f"{MANAGEMENT_BASE}/api/v1/telemetry/ingest/"
        payload = {
            "device_id": str(event.device_id),
            "livestock_id": str(event.livestock_id),
            "metric": event.metric,
            "value": event.value,
            "recorded_at": event.recorded_at.isoformat(),
        }
        r = requests.post(url, json=payload, timeout=3)
        r.raise_for_status()
