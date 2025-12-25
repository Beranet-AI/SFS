import uuid
from django.db import models
from django.utils import timezone


class DiscoveryStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class DeviceDiscoveryModel(models.Model):
    """
    Temporary record for devices discovered by edge/labview before approval.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    device_serial = models.CharField(max_length=128, unique=True, db_index=True)
    device_type = models.CharField(max_length=64, db_index=True)  # sensor/actuator type string
    display_name = models.CharField(max_length=128, blank=True, default="")

    manufacturer = models.CharField(max_length=128, blank=True, default="")
    model = models.CharField(max_length=128, blank=True, default="")
    firmware = models.CharField(max_length=64, blank=True, default="")

    capabilities = models.JSONField(default=dict, blank=True)  # metrics, commands, protocols...

    last_seen_at = models.DateTimeField(default=timezone.now)
    first_seen_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=16,
        choices=DiscoveryStatus.choices,
        default=DiscoveryStatus.PENDING,
        db_index=True,
    )

    raw_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "devices_device_discovery"
        indexes = [
            models.Index(fields=["device_serial"]),
            models.Index(fields=["status"]),
        ]
