import requests
from typing import Dict, Any
from backend.services.edge_controller.core.config import settings


class IngestionClient:
    def forward_telemetry(self, payload: Dict[str, Any]) -> None:
        url = f"{settings.DATA_INGESTION_BASE_URL}/ingest/telemetry"
        requests.post(url, json=payload, timeout=5)
