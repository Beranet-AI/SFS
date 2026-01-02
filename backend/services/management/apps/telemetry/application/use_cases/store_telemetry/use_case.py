# application/use_cases/store_telemetry/use_case.py

from datetime import datetime

from .input_dto import StoreTelemetryInputDTO
from .output_dto import StoreTelemetryOutputDTO
from ....infrastructure.models.telemetry_model import TelemetryModel
from ....infrastructure.mappers.telemetry_mapper import TelemetryMapper


class StoreTelemetryUseCase:
    """
    Persists validated telemetry
    """

    def __init__(self):
        self._mapper = TelemetryMapper()

    def execute(self, input_dto: StoreTelemetryInputDTO) -> StoreTelemetryOutputDTO:
        received_at = input_dto.received_at
        if isinstance(received_at, int):
            received_at = datetime.fromtimestamp(received_at)

        record = self._mapper.domain_to_record(
            device_id=input_dto.device_id,
            source=input_dto.source,
            schema_version=input_dto.schema_version,
            telemetry_data=input_dto.telemetry_data,
            received_at=received_at,
        )

        record.save()

        return StoreTelemetryOutputDTO(telemetry_id=str(record.id))
