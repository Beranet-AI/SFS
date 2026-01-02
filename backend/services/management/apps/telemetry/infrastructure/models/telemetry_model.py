import uuid
from django.db import models


class TelemetryModel(models.Model):
    """
    Immutable record of telemetry events.
    """

    class Source(models.TextChoices):
        EDGE_CONTROLLER = "EDGE_CONTROLLER", "Edge Controller"
        COMMAND_RESULT = "COMMAND_RESULT", "Command Result"
        INGESTION = "INGESTION", "Data Ingestion"
        MANAGEMENT = "MANAGEMENT", "Management Telemetry"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    device_id = models.CharField(
        max_length=128,
        db_index=True,
        help_text="Logical device identifier (from management.devices)",
    )
    device_type = models.CharField(max_length=64, db_index=True)
    metric = models.CharField(max_length=128, db_index=True)
    value = models.JSONField()
    unit = models.CharField(max_length=32, null=True, blank=True)

    source = models.CharField(max_length=32, choices=Source.choices)

    farm_id = models.CharField(max_length=64, null=True, blank=True)
    barn_id = models.CharField(max_length=64, null=True, blank=True)
    zone_id = models.CharField(max_length=64, null=True, blank=True)
    livestock_id = models.CharField(max_length=64, null=True, blank=True)

    schema_version = models.CharField(max_length=16, null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)

    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "telemetry_events"
        indexes = [
            models.Index(fields=["device_id", "recorded_at"]),
            models.Index(fields=["metric", "recorded_at"]),
        ]
