from datetime import datetime
from django.utils import timezone

from apps.telemetry.models import TelemetryModel


class TelemetryService:
    """
    Application service responsible for ingesting and querying telemetry data.
    Single source of truth for telemetry persistence.
    All ORM access lives here.
    """

    # -------------------------
    # Commands
    # -------------------------
    def ingest(
        self,
        *,
        device_id: str,
        livestock_id: str,
        metric: str,
        value: float,
        recorded_at: datetime | None = None,
    ) -> TelemetryModel:
        return TelemetryModel.objects.create(
            device_id=str(device_id),
            livestock_id=str(livestock_id),
            metric=metric,
            value=float(value),
            recorded_at=recorded_at or timezone.now(),
        )

    # -------------------------
    # Queries
    # -------------------------
    def list_recent(self, *, livestock_id: str, limit: int = 100):
        qs = (
            TelemetryModel.objects
            .filter(livestock_id=str(livestock_id))
            .order_by("-recorded_at")[: int(limit)]
        )
        return qs
