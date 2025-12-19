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
