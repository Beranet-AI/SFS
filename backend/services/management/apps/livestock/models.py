from django.db import models


class LivestockModel(models.Model):
    tag = models.CharField(max_length=64)

    farm_id = models.CharField(max_length=64)
    barn = models.CharField(max_length=64)
    zone = models.CharField(max_length=64)

    health_state = models.CharField(max_length=32, default="healthy")
    health_confidence = models.FloatField(default=1.0)
    health_evaluated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.tag


class LivestockSensorGroupModel(models.Model):
    livestock = models.OneToOneField(
        LivestockModel,
        on_delete=models.CASCADE,
        related_name="sensor_group",
    )
    rfid_device = models.OneToOneField(
        "devices.DeviceModel",
        on_delete=models.PROTECT,
        related_name="rfid_livestock_group",
    )
    sensors = models.ManyToManyField(
        "devices.DeviceModel",
        related_name="livestock_sensor_groups",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"LivestockSensorGroup({self.livestock_id})"
