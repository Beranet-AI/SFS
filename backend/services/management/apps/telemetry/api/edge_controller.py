# backend/services/management/apps/telemetry/api/edge_controller.py

import json
from django.views import View
from django.http import HttpRequest

from .base import BaseTelemetryController
from ..application.services.telemetry_service import TelemetryService
from ..application.use_cases.receive_telemetry.input_dto import (
    ReceiveTelemetryInputDTO,
)


class EdgeControllerTelemetryView(BaseTelemetryController, View):
    """
    Receives telemetry from Edge Controller.
    Includes:
    - sensor telemetry
    - command execution results
    """

    service = TelemetryService()

    def post(self, request: HttpRequest):
        try:
            payload = json.loads(request.body)

            input_dto = ReceiveTelemetryInputDTO(
                source="EDGE_CONTROLLER",
                device_id=payload.get("device_id"),
                payload=payload.get("payload"),
                received_at=payload.get("received_at"),
                metadata=payload.get("metadata", {}),
            )

            result = self.service.receive_telemetry(input_dto)

            return self.response_ok(
                {
                    "status": result.status,
                    "telemetry_id": result.telemetry_id,
                },
                status=201,
            )

        except Exception as exc:
            return self.response_error(str(exc), status=400)
