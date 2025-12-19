from django.db import models

class DeviceModel(models.Model):
    serial = models.CharField(max_length=128, unique=True)
    device_type = models.CharField(max_length=64)
    status = models.CharField(max_length=32)

    assigned_livestock_id = models.CharField(
        max_length=64, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.serial
