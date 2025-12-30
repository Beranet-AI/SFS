# backend/services/management/apps/telemetry/api/commands.py

import json
from django.views import View
from django.http import HttpRequest

from .base import BaseTelemetryController
from ..application.services.telemetry_service import TelemetryService
from ..application.use_cases.receive_telemetry.input_dto import (
    ReceiveTelemetryInputDTO,
)


class CommandResultTelemetryView(BaseTelemetryController, View):
    """
    Receives telemetry generated as result of command execution.
    Example:
    - valve opened
    - fan turned off
    - command timeout / error
    """

    service = TelemetryService()

    def post(self, request: HttpRequest):
        try:
            payload = json.loads(request.body)

            input_dto = ReceiveTelemetryInputDTO(
                source="COMMAND_RESULT",
                device_id=payload.get("device_id"),
                payload=payload.get("result"),
                received_at=payload.get("executed_at"),
                metadata={
                    "command_id": payload.get("command_id"),
                    "command_type": payload.get("command_type"),
                },
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
