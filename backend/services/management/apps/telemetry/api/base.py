# backend/services/management/apps/telemetry/api/base.py

from abc import ABC
from django.http import JsonResponse


class BaseTelemetryController(ABC):
    """
    Base controller for telemetry-related endpoints.
    Controllers must only:
    - extract request data
    - build input DTO
    - call application service
    """

    service = None  # TelemetryService injected by subclass

    def response_ok(self, data: dict, status: int = 200):
        return JsonResponse(data, status=status, safe=False)

    def response_error(self, message: str, status: int = 400):
        return JsonResponse({"error": message}, status=status)
