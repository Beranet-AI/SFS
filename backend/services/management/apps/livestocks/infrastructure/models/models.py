from django.db import models
from apps.farms.infrastructure.models.models import FarmModel


class LivestockModel(models.Model):
    farm = models.ForeignKey(
        FarmModel,
        on_delete=models.CASCADE,
        related_name="livestocks",
    )

    tag_id = models.CharField(max_length=64, unique=True)
    species = models.CharField(max_length=64)
    breed = models.CharField(max_length=64)
    birth_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "livestocks_livestockmodel"

    def __str__(self):
        return self.tag_id


class HealthRecordModel(models.Model):
    livestock = models.ForeignKey(
        LivestockModel,
        on_delete=models.CASCADE,
        related_name="health_records",
    )

    status = models.CharField(max_length=64)
    temperature = models.FloatField()
    recorded_at = models.DateTimeField()

    class Meta:
        db_table = "livestocks_healthrecordmodel"


class MilkRecordModel(models.Model):
    livestock = models.ForeignKey(
        LivestockModel,
        on_delete=models.CASCADE,
        related_name="milk_records",
    )

    amount_liters = models.FloatField()
    recorded_at = models.DateTimeField()

    class Meta:
        db_table = "livestocks_milkrecordmodel"


class DiseaseRecordModel(models.Model):
    livestock = models.ForeignKey(
        LivestockModel,
        on_delete=models.CASCADE,
        related_name="disease_records",
    )

    disease_name = models.CharField(max_length=128)
    severity = models.CharField(max_length=32)
    detected_at = models.DateTimeField()

    class Meta:
        db_table = "livestocks_diseaserecordmodel"
