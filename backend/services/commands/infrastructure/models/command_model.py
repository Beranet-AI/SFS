import uuid
from django.db import models
from django.utils import timezone


class CommandStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    ACKED = "acked", "Acknowledged"
    FAILED = "failed", "Failed"


class CommandSource(models.TextChoices):
    MANUAL = "manual", "Manual"
    AI = "ai", "AI"
    SYSTEM = "system", "System"


class CommandModel(models.Model):
    """
    Represents a command sent to an actuator (fan, valve, ozone injector, etc.)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    command_type = models.CharField(
        max_length=64,
        db_index=True
    )  # FAN_SET_SPEED, VALVE_OPEN, etc.

    target_device_serial = models.CharField(
        max_length=128,
        db_index=True
    )

    params = models.JSONField(default=dict, blank=True)

    status = models.CharField(
        max_length=16,
        choices=CommandStatus.choices,
        default=CommandStatus.PENDING,
        db_index=True,
    )

    source = models.CharField(
        max_length=16,
        choices=CommandSource.choices,
        default=CommandSource.MANUAL,
    )

    issued_by = models.CharField(
        max_length=64,
        default="admin",
    )

    correlation_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        db_index=True,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "commands_command"
        indexes = [
            models.Index(fields=["target_device_serial"]),
            models.Index(fields=["status"]),
        ]
