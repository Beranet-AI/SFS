import requests
from typing import Dict, Any
from data_ingestion.core.config import settings

class ManagementClient:
    def upsert_discovery(self, payload: Dict[str, Any]) -> None:
        url = f"{settings.MANAGEMENT_BASE_URL}/api/discovery/devices"
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()

    def report_incident(self, payload: Dict[str, Any]) -> None:
        url = f"{settings.MANAGEMENT_BASE_URL}/api/incidents"
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
