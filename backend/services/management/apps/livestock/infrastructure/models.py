from django.db import models
import uuid
from core.models.farm import Farm
from core.models.barn import Barn
from core.models.zone import Zone

class Livestock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tag_id = models.CharField(max_length=100, unique=True)
    species = models.CharField(max_length=50)   # cow, sheep, goat
    breed = models.CharField(max_length=100, null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.SET_NULL)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.species} ({self.tag_id})"
