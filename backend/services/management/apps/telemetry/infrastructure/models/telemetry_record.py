# backend/services/management/apps/telemetry/infrastructure/models/telemetry_record.py

import uuid
from django.db import models


class TelemetryRecord(models.Model):
    """
    Immutable record of validated telemetry.
    Source of truth for audit, analysis, and reprocessing.
    """

    class Source(models.TextChoices):
        EDGE_CONTROLLER = "EDGE_CONTROLLER", "Edge Controller"
        COMMAND_RESULT = "COMMAND_RESULT", "Command Result"
        INGESTION = "INGESTION", "Data Ingestion"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    device_id = models.CharField(
        max_length=128,
        db_index=True,
        help_text="Logical device identifier (from management.devices)",
    )

    source = models.CharField(
        max_length=32,
        choices=Source.choices,
    )