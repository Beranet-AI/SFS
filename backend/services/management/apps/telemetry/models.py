from django.db import models


class TelemetryModel(models.Model):
    device_id = models.CharField(max_length=64)
    livestock_id = models.CharField(max_length=64)

    metric = models.CharField(max_length=64)
    value = models.FloatField()

    recorded_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["livestock_id", "recorded_at"]),
            models.Index(fields=["device_id", "recorded_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.livestock_id} | {self.metric}={self.value}"
