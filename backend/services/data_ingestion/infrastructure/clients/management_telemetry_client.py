from typing import Dict, Any

from backend.services.data_ingestion.core.config import settings


class ManagementTelemetryClient:
    def request_validation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "valid": True,
            "details": None,
            "management_base_url": settings.MANAGEMENT_BASE_URL,
        }
