import requests
from apps.integrations.infrastructure.settings import INGESTION_BASE, TIMEOUT_SEC


class IngestionClient:
    """
    Infrastructure HTTP client for Data Ingestion service.
    """

    def ping(self) -> dict:
        try:
            response = requests.get(
                f"{INGESTION_BASE}/health",
                timeout=TIMEOUT_SEC,
            )
            return {
                "ok": response.ok,
                "status": response.status_code,
            }
        except requests.RequestException as exc:
            return {
                "ok": False,
                "error": str(exc),
            }
