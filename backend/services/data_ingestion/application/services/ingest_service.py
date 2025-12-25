from typing import Dict, Any
from data_ingestion.core.config import settings
import requests


class IngestService:
    def push_livestatus(self, telemetry: Dict[str, Any]) -> None:
        if not settings.ENABLE_LIVESTATUS_PUSH:
            return
        url = f"{settings.MONITORING_BASE_URL}/monitoring/livestatus/push"
        requests.post(url, json=telemetry, timeout=3)
