
from django.db import models
import uuid
from .farm import Farm

class Barn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="barns")

    name = models.CharField(max_length=200)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.farm.name} / {self.name}"
