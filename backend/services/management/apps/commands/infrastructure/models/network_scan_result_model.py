import uuid

from django.db import models


class NetworkScanResultModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scan_id = models.UUIDField(db_index=True)
    device_uid = models.CharField(max_length=128)
    device_name = models.CharField(max_length=255, null=True, blank=True)
    device_category = models.CharField(max_length=64)
    device_type = models.CharField(max_length=64)
    protocol = models.CharField(max_length=64, blank=True, default="")
    adapter_type = models.CharField(max_length=64, blank=True, default="")
    direction = models.CharField(
        max_length=32,
        choices=[("uplink_only", "Uplink Only"), ("bidirectional", "Bidirectional")],
    )
    supports_commands = models.BooleanField(default=False)
    supported_command_categories = models.JSONField(blank=True, default=list)
    ip_address = models.CharField(max_length=64, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    network_address = models.CharField(max_length=128, null=True, blank=True)
    signal_strength = models.FloatField(null=True, blank=True)
    firmware_version = models.CharField(max_length=128, null=True, blank=True)
    vendor = models.CharField(max_length=128, null=True, blank=True)
    model = models.CharField(max_length=128, null=True, blank=True)
    battery_level = models.FloatField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    discovered_at = models.DateTimeField(null=True, blank=True)
    scan_status = models.CharField(
        max_length=16,
        choices=[("new", "New"), ("known", "Known"), ("changed", "Changed")],
        default="new",
    )
    raw_capabilities = models.JSONField(null=True, blank=True)
    is_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "commands"
        db_table = "commands_network_scan_result"
        ordering = ["-discovered_at", "-created_at"]
        verbose_name = "Discover"
        verbose_name_plural = "Discover"
        constraints = [
            models.UniqueConstraint(
                fields=("scan_id", "device_uid"),
                name="uniq_network_scan_device",
            )
        ]
        indexes = [
            models.Index(fields=["scan_id", "device_uid"]),
            models.Index(fields=["scan_status"]),
            models.Index(fields=["is_registered"]),
        ]
