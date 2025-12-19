from django.db import models

class IncidentModel(models.Model):
    livestock_id = models.CharField(max_length=64)
    severity = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    source = models.CharField(max_length=32)
    description = models.TextField()

    created_at = models.DateTimeField()
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["livestock_id", "status"]),
            models.Index(fields=["severity", "status"]),
        ]
