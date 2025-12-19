import requests
from apps.integrations.infrastructure.settings import INGESTION_BASE, TIMEOUT_SEC

class IngestionClient:
    def ping(self) -> dict:
        try:
            r = requests.get(f"{INGESTION_BASE}/health", timeout=TIMEOUT_SEC)
            return {"ok": r.ok, "status": r.status_code}
        except Exception as e:
            return {"ok": False, "error": str(e)}
