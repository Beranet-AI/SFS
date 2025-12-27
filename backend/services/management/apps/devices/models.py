from django.db import models
from django.utils import timezone


class DeviceStatus(models.TextChoices):
    DISCOVERED = "discovered", "Discovered"
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DISABLED = "disabled", "Disabled"


class DeviceModel(models.Model):
    serial = models.CharField(max_length=128, unique=True)
    kind = models.CharField(max_length=64)

    display_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=32,
        choices=DeviceStatus.choices,
        default=DeviceStatus.DISCOVERED,
    )

    farm_id = models.CharField(max_length=64, null=True, blank=True)
    barn_id = models.CharField(max_length=64, null=True, blank=True)
    zone_id = models.CharField(max_length=64, null=True, blank=True)
    livestock_id = models.CharField(max_length=64, null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)
    capabilities = models.JSONField(default=dict, blank=True)

    last_seen_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------
    # Lifecycle helpers
    # -------------------------

    def mark_seen(self) -> None:
        self.last_seen_at = timezone.now()
        self.save(update_fields=["last_seen_at"])

    def change_status(self, status: DeviceStatus) -> None:
        self.status = status
        self.save(update_fields=["status"])

    def assign(
        self,
        *,
        farm_id: str | None = None,
        barn_id: str | None = None,
        zone_id: str | None = None,
        livestock_id: str | None = None,
    ) -> None:
        self.farm_id = farm_id
        self.barn_id = barn_id
        self.zone_id = zone_id
        self.livestock_id = livestock_id
        self.save(
            update_fields=["farm_id", "barn_id", "zone_id", "livestock_id"]
        )

    def __str__(self) -> str:
        return f"{self.serial} ({self.kind})"
