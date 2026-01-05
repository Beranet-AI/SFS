import uuid

from django.db import models
from django.utils import timezone

from apps.devices.models import DeviceModel

from .command_model import CommandModel


class DiscoverySessionModel(models.Model):
    """Retained for backwards compatibility with discovery sessions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    edge_node_id = models.CharField(max_length=64)
    status = models.CharField(
        max_length=16,
        choices=[
            ("pending", "Pending"),
            ("running", "Running"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ],
        default="pending",
        db_index=True,
    )
    started_by = models.CharField(max_length=64, blank=True, default="")
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    device_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, default="")
    command = models.ForeignKey(
        CommandModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="discovery_sessions",
    )

    class Meta:
        app_label = "commands"
        db_table = "commands_discovery_session"
        ordering = ["-started_at"]
        verbose_name = "Discover Devices"
        verbose_name_plural = "Discover Devices"


class DiscoveredDeviceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        DiscoverySessionModel,
        on_delete=models.CASCADE,
        related_name="devices",
    )
    device_id = models.CharField(max_length=128)
    device_type = models.CharField(max_length=128, blank=True, default="")
    ip_address = models.CharField(max_length=64, blank=True, default="")
    capabilities = models.JSONField(blank=True, default=dict)
    raw_payload = models.JSONField(blank=True, default=dict)
    status = models.CharField(
        max_length=16,
        choices=[("new", "New"), ("registered", "Registered")],
        default="new",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registered_device = models.ForeignKey(
        DeviceModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="discovery_records",
    )

    class Meta:
        app_label = "commands"
        db_table = "commands_discovered_device"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=("session", "device_id"),
                name="uniq_discovery_session_device",
            )
        ]
        indexes = [
            models.Index(fields=["session", "device_id"]),
            models.Index(fields=["status"]),
        ]


NetworkScanResultModel = DiscoveredDeviceModel
