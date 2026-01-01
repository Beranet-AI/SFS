# mappers/telemetry_mapper.py

from ..infrastructure.models.telemetry_record import TelemetryRecord
from ..infrastructure.models.telemetry_schema import TelemetrySchema

class TelemetryMapper:
    def raw_to_domain(self, raw: dict) -> dict:
        return raw

    def domain_to_record(
        self,
        device_id: str,
        source: str,
        schema_version: str,
        telemetry_data: dict,
        received_at: int,
    ) -> TelemetryRecord:
        return TelemetryRecord(
            device_id=device_id,
            source=source,
            schema_version=schema_version,
            telemetry_data=telemetry_data,
            received_at=received_at,
        )
