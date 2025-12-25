import requests
from typing import Dict, Any
from data_ingestion.core.config import settings

class MonitoringClient:
    def push_livestatus(self, payload: Dict[str, Any]) -> None:
        url = f"{settings.MONITORING_BASE_URL}/monitoring/livestatus"
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
