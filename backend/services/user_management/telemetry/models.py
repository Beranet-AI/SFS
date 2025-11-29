from django.db import models

# Create your models here.

from devices.models import Sensor


class SensorReading(models.Model):
    QUALITY_CHOICES = (
        ("good", "Good"),
        ("bad", "Bad"),
        ("suspect", "Suspect"),
    )

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="readings",
    )
    ts = models.DateTimeField(
        db_index=True,
        help_text="زمان ثبت نمونه (timestamp)"
    )
    value = models.FloatField(
        help_text="مقدار اندازه‌گیری شده"
    )

    raw_payload = models.JSONField(
        null=True,
        blank=True,
        help_text="داده خام دریافتی از سنسور/پروتکل (در صورت نیاز)"
    )

    quality = models.CharField(
        max_length=10,
        choices=QUALITY_CHOICES,
        default="good",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sensor_readings"
        verbose_name = "Sensor Reading"
        verbose_name_plural = "Sensor Readings"
        indexes = [
            models.Index(fields=["sensor", "ts"]),
        ]
        ordering = ["-ts"]

    def __str__(self) -> str:
        return f"{self.sensor} @ {self.ts} = {self.value}"

