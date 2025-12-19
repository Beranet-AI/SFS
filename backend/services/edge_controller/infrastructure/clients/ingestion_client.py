import requests
from edge_controller.core.config import DATA_INGESTION_BASE

class IngestionClient:
    def push_telemetry(self, payload: dict):
        url = f"{DATA_INGESTION_BASE}/api/v1/telemetry/ingest/"
        r = requests.post(url, json=payload, timeout=3)
        r.raise_for_status()
