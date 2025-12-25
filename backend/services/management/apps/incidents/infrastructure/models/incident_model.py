import uuid
from django.db import models
from django.utils import timezone


class IncidentStatus(models.TextChoices):
    OPEN = "open", "Open"
    ACK = "ack", "Acknowledged"
    RESOLVED = "resolved", "Resolved"


class IncidentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=80, db_index=True)
    severity = models.CharField(max_length=16, db_index=True)  # low|medium|high|critical
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")

    status = models.CharField(max_length=16, choices=IncidentStatus.choices, default=IncidentStatus.OPEN)

    device_serial = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    livestock_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    farm_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    barn_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    zone_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)

    evidence = models.JSONField(default=dict, blank=True)

    ts = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "incidents_incident"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["severity"]),
        ]
