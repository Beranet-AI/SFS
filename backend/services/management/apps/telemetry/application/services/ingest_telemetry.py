from apps.telemetry.domain.records.telemetry_record import TelemetryRecord
from datetime import datetime

class IngestTelemetryService:
    """
    Application service responsible for receiving telemetry
    and persisting it.
    """

    def __init__(self, repo):
        self.repo = repo

    def ingest(
        self,
        device_id,
        livestock_id,
        metric: str,
        value: float,
        recorded_at: datetime | None = None,
    ):
        record = TelemetryRecord(
            device_id=device_id,
            livestock_id=livestock_id,
            metric=metric,
            value=value,
            recorded_at=recorded_at or datetime.utcnow(),
        )
        self.repo.save(record)
        return record
