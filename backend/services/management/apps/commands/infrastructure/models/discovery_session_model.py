import uuid

from django.db import models
from django.utils import timezone

from apps.commands.infrastructure.models.command_model import CommandModel


class DiscoverySessionStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    RUNNING = "running", "Running"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"


class DiscoverySessionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    edge_node_id = models.CharField(max_length=64)
    command = models.ForeignKey(
        CommandModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="discovery_sessions",
    )
    status = models.CharField(
        max_length=16,
        choices=DiscoverySessionStatusChoices.choices,
        default=DiscoverySessionStatusChoices.PENDING,
        db_index=True,
    )
    started_by = models.CharField(max_length=64, blank=True, default="")
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    device_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, default="")

    class Meta:
        app_label = "commands"
        db_table = "commands_discovery_session"
        ordering = ["-started_at"]
        verbose_name = "Discover Devices"
        verbose_name_plural = "Discover Devices"
        indexes = [
            models.Index(fields=["edge_node_id", "started_at"]),
            models.Index(fields=["status"]),
        ]

    def mark_running(self) -> None:
        self.status = DiscoverySessionStatusChoices.RUNNING
        self.save(update_fields=["status"])

    def mark_completed(self, *, device_count: int) -> None:
        self.status = DiscoverySessionStatusChoices.COMPLETED
        self.device_count = device_count
        self.finished_at = timezone.now()
        self.save(update_fields=["status", "device_count", "finished_at"])

    def mark_failed(self, *, error_message: str) -> None:
        self.status = DiscoverySessionStatusChoices.FAILED
        self.error_message = error_message
        self.finished_at = timezone.now()
        self.save(update_fields=["status", "error_message", "finished_at"])
