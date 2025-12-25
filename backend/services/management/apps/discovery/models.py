from django.db import models

class DeviceDiscoveryModel(models.Model):
    """
    هر چیزی که edge کشف می‌کند اینجا می‌آید تا دستی approve شود.
    """
    external_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=120)
    device_type = models.CharField(max_length=64)
    protocol = models.CharField(max_length=32)
    role = models.CharField(max_length=16)  # sensor/actuator/gateway

    ip = models.GenericIPAddressField(null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    last_seen = models.DateTimeField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.device_type})"
