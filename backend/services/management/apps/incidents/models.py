# apps/incidents/models.py
import uuid
from django.db import models
from django.utils import timezone


class IncidentSeverity(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class IncidentStatus(models.TextChoices):
    OPEN = "open", "Open"
    ACKNOWLEDGED = "acknowledged", "Acknowledged"
    RESOLVED = "resolved", "Resolved"
    CLOSED = "closed", "Closed"


class IncidentModel(models.Model):
    """
    Django ORM model (single source of truth for persistence).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    source = models.CharField(max_length=64)
    source_ref = models.CharField(max_length=128, blank=True, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    severity = models.CharField(
        max_length=16,
        choices=IncidentSeverity.choices,
        default=IncidentSeverity.MEDIUM,
    )

    status = models.CharField(
        max_length=16,
        choices=IncidentStatus.choices,
        default=IncidentStatus.OPEN,
    )

    device_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    livestock_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)

    occurred_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "incidents_incident"
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["severity"]),
            models.Index(fields=["status"]),
            models.Index(fields=["device_id"]),
        ]

    def acknowledge(self):
        self.status = IncidentStatus.ACKNOWLEDGED
        self.save(update_fields=["status", "updated_at"])

    def resolve(self):
        self.status = IncidentStatus.RESOLVED
        self.save(update_fields=["status", "updated_at"])
