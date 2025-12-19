import requests
from apps.integrations.infrastructure.settings import MONITORING_BASE, TIMEOUT_SEC

class MonitoringClient:
    def ping(self) -> dict:
        try:
            r = requests.get(f"{MONITORING_BASE}/health", timeout=TIMEOUT_SEC)
            return {"ok": r.ok, "status": r.status_code}
        except Exception as e:
            return {"ok": False, "error": str(e)}
