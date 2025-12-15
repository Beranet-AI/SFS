from django.db import models
import uuid
from .barn import Barn

class Zone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE, related_name="zones")

    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.barn.name} / {self.name}"
