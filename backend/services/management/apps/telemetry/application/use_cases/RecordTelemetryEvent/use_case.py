from .record_telemetry_event_input import RecordTelemetryEventInput
from .record_telemetry_event_output import RecordTelemetryEventOutput
from ....infrastructure.models.telemetry_model import TelemetryModel


class RecordTelemetryEventUseCase:
    def execute(
        self, input_dto: RecordTelemetryEventInput
    ) -> RecordTelemetryEventOutput:
        records = [
            TelemetryModel(
                device_id=item.get("device_id", ""),
                device_type=item.get("device_type", ""),
                metric=item.get("metric", ""),
                value=item.get("value"),
                unit=item.get("unit"),
                source=item.get("source", "MANAGEMENT"),
                farm_id=item.get("farm_id"),
                barn_id=item.get("barn_id"),
                zone_id=item.get("zone_id"),
                livestock_id=item.get("livestock_id"),
                schema_version=item.get("schema_version"),
                payload=item.get("payload") or {},
                recorded_at=item.get("recorded_at"),
            )
            for item in input_dto.standardized
        ]

        TelemetryModel.objects.bulk_create(records)

        return RecordTelemetryEventOutput(recorded_count=len(records))
