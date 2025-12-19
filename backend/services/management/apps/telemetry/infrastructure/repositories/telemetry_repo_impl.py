from apps.telemetry.domain.records.telemetry_record import TelemetryRecord
from apps.telemetry.infrastructure.models.telemetry_model import TelemetryModel

class DjangoTelemetryRepository:

    def save(self, record: TelemetryRecord) -> None:
        TelemetryModel.objects.create(
            device_id=str(record.device_id),
            livestock_id=str(record.livestock_id),
            metric=record.metric,
            value=record.value,
            recorded_at=record.recorded_at,
        )

    def list_recent(self, livestock_id: str, limit: int = 100):
        qs = (
            TelemetryModel.objects
            .filter(livestock_id=livestock_id)
            .order_by("-recorded_at")[:limit]
        )
        return list(qs.values())
