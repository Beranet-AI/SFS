import uuid

from django.db import models

from apps.commands.infrastructure.models.discovery_session_model import (
    DiscoverySessionModel,
)
from apps.devices.models import DeviceModel


class DiscoveredDeviceStatusChoices(models.TextChoices):
    NEW = "new", "New"
    REGISTERED = "registered", "Registered"


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
    capabilities = models.JSONField(default=dict, blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=16,
        choices=DiscoveredDeviceStatusChoices.choices,
        default=DiscoveredDeviceStatusChoices.NEW,
    )
    registered_device = models.ForeignKey(
        DeviceModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="discovery_records",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "commands"
        db_table = "commands_discovered_device"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["session", "device_id"],
                name="uniq_discovery_session_device",
            )
        ]
        indexes = [
            models.Index(fields=["session", "device_id"]),
            models.Index(fields=["status"]),
        ]

    def mark_registered(self, *, registered_device: DeviceModel) -> None:
        self.status = DiscoveredDeviceStatusChoices.REGISTERED
        self.registered_device = registered_device
        self.save(update_fields=["status", "registered_device", "updated_at"])
