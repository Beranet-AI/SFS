# application/use_cases/store_telemetry/use_case.py

from .input_dto import StoreTelemetryInputDTO
from .output_dto import StoreTelemetryOutputDTO
from ....models.telemetry_record import TelemetryRecord
from ....mappers.telemetry_mapper import TelemetryMapper


class StoreTelemetryUseCase:
    """
    Persists validated telemetry
    """

    def __init__(self):
        self._mapper = TelemetryMapper()

    def execute(self, input_dto: StoreTelemetryInputDTO) -> StoreTelemetryOutputDTO:
        record = self._mapper.domain_to_record(
            device_id=input_dto.device_id,
            source=input_dto.source,
            schema_version=input_dto.schema_version,
            telemetry_data=input_dto.telemetry_data,
            received_at=input_dto.received_at,
        )

        record.save()

        return StoreTelemetryOutputDTO(telemetry_id=str(record.id))
