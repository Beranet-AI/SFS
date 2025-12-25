import uuid
from django.db import models
from django.utils import timezone


class DeviceKind(models.TextChoices):
    SENSOR = "sensor", "Sensor"
    ACTUATOR = "actuator", "Actuator"
    GATEWAY = "gateway", "Gateway"


class DeviceStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DISABLED = "disabled", "Disabled"


class DeviceProtocol(models.TextChoices):
    HTTP_JSON = "http_json", "HTTP JSON"
    MQTT = "mqtt", "MQTT"
    MODBUS = "modbus", "Modbus"
    OPCUA = "opcua", "OPC UA"
    LABVIEW = "labview", "LabVIEW"


class ApprovalStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class DeviceModel(models.Model):
    """
    Infrastructure persistence model.
    Clean/DDD note: Domain entity != Django model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # unique identity on the edge network
    serial = models.CharField(max_length=128, unique=True, db_index=True)

    # classification
    kind = models.CharField(max_length=32, choices=DeviceKind.choices, default=DeviceKind.SENSOR)
    device_type = models.CharField(max_length=64, db_index=True)  # temperature, fan, valve, etc.
    protocol = models.CharField(max_length=32, choices=DeviceProtocol.choices, default=DeviceProtocol.HTTP_JSON)

    display_name = models.CharField(max_length=200, blank=True, default="")

    status = models.CharField(max_length=32, choices=DeviceStatus.choices, default=DeviceStatus.PENDING)
    approval_status = models.CharField(max_length=32, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)

    # assignment (you said it connects to farm/barn/zone + sometimes livestock)
    farm_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    barn_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    zone_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    livestock_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)

    # capabilities and metadata (extensible industrial style)
    capabilities = models.JSONField(default=dict, blank=True)  # supported metrics/commands/etc.
    metadata = models.JSONField(default=dict, blank=True)      # vendor, fw, model, etc.

    # health/heartbeat
    last_seen_at = models.DateTimeField(blank=True, null=True)
    heartbeat_interval_sec = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "devices_device"
        indexes = [
            models.Index(fields=["device_type"]),
            models.Index(fields=["kind"]),
            models.Index(fields=["status"]),
        ]

    def mark_seen(self):
        self.last_seen_at = timezone.now()
        self.save(update_fields=["last_seen_at", "updated_at"])
