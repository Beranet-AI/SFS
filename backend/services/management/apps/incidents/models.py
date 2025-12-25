from django.db import models

class IncidentModel(models.Model):
    severity = models.CharField(max_length=16)  # low/medium/high/critical
    status = models.CharField(max_length=16, default="open")  # open/acked/resolved

    title = models.CharField(max_length=200)
    description = models.TextField()

    device_id = models.IntegerField(null=True, blank=True)
    farm_id = models.CharField(max_length=64, null=True, blank=True)
    barn_id = models.CharField(max_length=64, null=True, blank=True)
    zone_id = models.CharField(max_length=64, null=True, blank=True)
    livestock_id = models.CharField(max_length=64, null=True, blank=True)

    context = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.severity}] {self.title}"
