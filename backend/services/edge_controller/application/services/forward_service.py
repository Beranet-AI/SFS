from typing import Dict, Any
from edge_controller.core.config import settings
from edge_controller.infrastructure.clients.ingestion_client import IngestionClient


class ForwardService:
    def __init__(self, ingest: IngestionClient):
        self.ingest = ingest

    def forward_telemetry(self, telemetry: Dict[str, Any]) -> None:
        if not settings.ENABLE_TELEMETRY_FORWARD:
            return
        self.ingest.forward_telemetry(telemetry)
