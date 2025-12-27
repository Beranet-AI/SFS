import requests
from typing import Dict, Any
from backend.services.edge_controller.core.config import settings


class ManagementClient:
    def upsert_discovery(self, payload: Dict[str, Any]) -> None:
        url = f"{settings.MANAGEMENT_BASE_URL}/devices/discoveries/upsert/"
        requests.post(url, json=payload, timeout=5)

    def create_incident(self, payload: Dict[str, Any]) -> None:
        url = f"{settings.MANAGEMENT_BASE_URL}/incidents/create/"
        requests.post(url, json=payload, timeout=5)
