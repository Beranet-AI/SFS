from django.db import models


class EventModel(models.Model):
    severity = models.CharField(max_length=16)
    status = models.CharField(max_length=16)

    title = models.CharField(max_length=255)
    message = models.TextField()

    metric = models.CharField(max_length=64, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)

    farm_id = models.UUIDField()
    barn_id = models.UUIDField(null=True, blank=True)
    zone_id = models.UUIDField(null=True, blank=True)
    device_id = models.UUIDField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "events"
        ordering = ["-created_at"]
