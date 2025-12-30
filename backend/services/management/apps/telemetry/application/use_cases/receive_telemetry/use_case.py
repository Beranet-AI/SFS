# application/use_cases/receive_telemetry/use_case.py

from .input_dto import ReceiveTelemetryInputDTO
from .output_dto import ReceiveTelemetryOutputDTO
from ..validate_telemetry.use_case import ValidateTelemetryUseCase
from ..store_telemetry.use_case import StoreTelemetryUseCase
from ..store_telemetry.input_dto import StoreTelemetryInputDTO


class ReceiveTelemetryUseCase:
    """
    Entry point for all telemetry
    """

    def __init__(self):
        self._validate_uc = ValidateTelemetryUseCase()
        self._store_uc = StoreTelemetryUseCase()

    def execute(
        self, input_dto: ReceiveTelemetryInputDTO
    ) -> ReceiveTelemetryOutputDTO:
        validated = self._validate_uc.execute(
            raw_payload=input_dto.payload,
            device_id=input_dto.device_id,
        )

        store_result = self._store_uc.execute(
            StoreTelemetryInputDTO(
                device_id=input_dto.device_id,
                source=input_dto.source,
                schema_version=validated.schema_version,
                telemetry_data=validated.domain_telemetry,
                received_at=input_dto.received_at,
            )
        )

        return ReceiveTelemetryOutputDTO(
            telemetry_id=store_result.telemetry_id,
            status="ACCEPTED",
        )
