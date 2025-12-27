import uuid
from django.db import models
from django.utils import timezone


class DiscoveryStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class DiscoveredDeviceRole(models.TextChoices):
    SENSOR = "sensor", "Sensor"
    ACTUATOR = "actuator", "Actuator"
    GATEWAY = "gateway", "Gateway"


class DeviceDiscoveryModel(models.Model):
    """
    Temporary record for devices discovered by edge layer
    before being promoted to real Device.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # identity
    device_serial = models.CharField(max_length=128, unique=True, db_index=True)
    device_type = models.CharField(max_length=64, db_index=True)
    display_name = models.CharField(max_length=128, blank=True, default="")

    # classification
    role = models.CharField(
        max_length=16,
        choices=DiscoveredDeviceRole.choices,
        default=DiscoveredDeviceRole.SENSOR,
    )

    protocol = models.CharField(max_length=32, blank=True, default="")
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # vendor / firmware
    manufacturer = models.CharField(max_length=128, blank=True, default="")
    model = models.CharField(max_length=128, blank=True, default="")
    firmware = models.CharField(max_length=64, blank=True, default="")

    # capabilities & raw payload
    capabilities = models.JSONField(default=dict, blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)

    # lifecycle
    first_seen_at = models.DateTimeField(default=timezone.now)
    last_seen_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=16,
        choices=DiscoveryStatus.choices,
        default=DiscoveryStatus.PENDING,
        db_index=True,
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "devices_device_discovery"
        ordering = ["-last_seen_at"]
        indexes = [
            models.Index(fields=["device_serial"]),
            models.Index(fields=["device_type"]),
            models.Index(fields=["status"]),
        ]

    def approve(self):
        if self.status != DiscoveryStatus.APPROVED:
            self.status = DiscoveryStatus.APPROVED
            self.approved_at = timezone.now()
            self.save(update_fields=["status", "approved_at"])

    def mark_seen(self):
        self.last_seen_at = timezone.now()
        self.save(update_fields=["last_seen_at"])

    def __str__(self) -> str:
        return f"{self.device_serial} ({self.device_type})"
