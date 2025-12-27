from django.db import models

class MedicalRecordModel(models.Model):
    livestock_id = models.CharField(max_length=64)
    diagnosis = models.CharField(max_length=64)
    notes = models.TextField()
    recorded_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.livestock_id} - {self.diagnosis}"
