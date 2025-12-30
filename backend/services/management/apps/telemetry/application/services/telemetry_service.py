# backend/services/management/apps/telemetry/application/services/telemetry_service.py

from ..use_cases.receive_telemetry.use_case import ReceiveTelemetryUseCase
from ..use_cases.receive_telemetry.input_dto import ReceiveTelemetryInputDTO
from ..use_cases.receive_telemetry.output_dto import ReceiveTelemetryOutputDTO


class TelemetryService:
    """
    Application Service (Orchestrator)

    Coordinates telemetry flow:
    - receive
    - validate
    - store
    """

    def __init__(self):
        self._receive_uc = ReceiveTelemetryUseCase()

    def receive_telemetry(
        self, input_dto: ReceiveTelemetryInputDTO
    ) -> ReceiveTelemetryOutputDTO:
        return self._receive_uc.execute(input_dto)
