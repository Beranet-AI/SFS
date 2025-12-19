import requests
from apps.integrations.infrastructure.settings import EDGE_BASE, TIMEOUT_SEC

class EdgeClient:
    def ping(self) -> dict:
        try:
            r = requests.get(f"{EDGE_BASE}/health", timeout=TIMEOUT_SEC)
            return {"ok": r.ok, "status": r.status_code}
        except Exception as e:
            return {"ok": False, "error": str(e)}
