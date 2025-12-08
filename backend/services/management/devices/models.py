from django.db import models

# Create your models here.

from farm.models import Farm, Barn, Zone


class Device(models.Model):
    DEVICE_TYPES = (
        ("edge_controller", "Edge Controller"),
        ("sensor_node", "Sensor Node"),
        ("camera", "Camera"),
        ("gateway", "Gateway"),
        ("other", "Other"),
    )

    STATUS_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
        ("fault", "Fault"),
        ("unknown", "Unknown"),
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="devices",
    )
    barn = models.ForeignKey(
        Barn,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devices",
    )
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devices",
    )

    type = models.CharField(
        max_length=50,
        choices=DEVICE_TYPES,
    )
    name = models.CharField(
        max_length=200,
        help_text="نام منطقی دستگاه (مثلاً edge-01 یا node-02)",
    )
    serial_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unknown",
    )
    last_seen_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "devices"
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        indexes = [
            models.Index(fields=["farm", "barn", "zone"]),
            models.Index(fields=["type", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"


class SensorType(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="temperature, humidity, ammonia, rfid, camera, ..."
    )
    name = models.CharField(max_length=100)
    unit = models.CharField(
        max_length=20,
        help_text="°C, %, ppm, ..."
    )
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "sensor_types"
        verbose_name = "Sensor Type"
        verbose_name_plural = "Sensor Types"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Sensor(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="sensors",
    )
    sensor_type = models.ForeignKey(
        SensorType,
        on_delete=models.PROTECT,
        related_name="sensors",
    )
    name = models.CharField(
        max_length=200,
        help_text="نام منطقی سنسور (مثلاً Barn1-Temp-01)",
    )
    hardware_address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="آدرس فیزیکی: کانال، پورت، Modbus address و ...",
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sensors"
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"
        indexes = [
            models.Index(fields=["device", "sensor_type"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} [{self.sensor_type.code}]"
