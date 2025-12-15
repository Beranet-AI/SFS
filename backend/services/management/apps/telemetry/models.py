from django.db import models
import uuid
from devices.models import Device

class TelemetryReading(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    metric = models.CharField(max_length=50)
    value = models.FloatField()
    unit = models.CharField(max_length=20)

    timestamp = models.DateTimeField()
    received_at = models.DateTimeField(auto_now_add=True)

    edge_id = models.UUIDField()

    def __str__(self):
        return f"{self.metric}={self.value}"
