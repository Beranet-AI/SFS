# livestock/infrastructure/models.py
from django.db import models


class LivestockModel(models.Model):
    tag_id = models.CharField(max_length=64, unique=True)
    breed = models.CharField(max_length=64)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=16)
    herd_entry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, default="ACTIVE")

    # Health snapshot
    temperature_c = models.FloatField(null=True, blank=True)
    activity = models.FloatField(null=True, blank=True)
    rumination_minutes = models.FloatField(null=True, blank=True)
    movement_index = models.FloatField(null=True, blank=True)
    lying_minutes = models.FloatField(null=True, blank=True)
    standing_minutes = models.FloatField(null=True, blank=True)
    heart_rate_bpm = models.IntegerField(null=True, blank=True)

    # Nutrition snapshot
    feed_intake_kg = models.FloatField(null=True, blank=True)
    water_intake_l = models.FloatField(null=True, blank=True)
    feeder_station_id = models.CharField(max_length=64, null=True, blank=True)

    # Milk snapshot
    milk_volume_l = models.FloatField(null=True, blank=True)
    milk_ec = models.FloatField(null=True, blank=True)
    milk_temp_c = models.FloatField(null=True, blank=True)
    milk_scc = models.IntegerField(null=True, blank=True)

    # Reproduction snapshot
    estrus = models.BooleanField(default=False)
    pregnant = models.BooleanField(default=False)
    insemination_date = models.DateField(null=True, blank=True)
    insemination_method = models.CharField(max_length=16, null=True, blank=True)
    insemination_result = models.CharField(max_length=16, null=True, blank=True)
    calving_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HealthRecordModel(models.Model):
    livestock = models.ForeignKey(LivestockModel, on_delete=models.CASCADE, related_name="health_records")
    temperature_c = models.FloatField()
    activity = models.FloatField()
    rumination_minutes = models.FloatField(null=True, blank=True)
    movement_index = models.FloatField(null=True, blank=True)
    lying_minutes = models.FloatField(null=True, blank=True)
    standing_minutes = models.FloatField(null=True, blank=True)
    heart_rate_bpm = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)


class MilkRecordModel(models.Model):
    livestock = models.ForeignKey(LivestockModel, on_delete=models.CASCADE, related_name="milk_records")
    volume_l = models.FloatField()
    ec = models.FloatField()
    milk_temp_c = models.FloatField(null=True, blank=True)
    scc = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)


class DiseaseRecordModel(models.Model):
    livestock = models.ForeignKey(LivestockModel, on_delete=models.CASCADE, related_name="disease_records")
    disease_name = models.CharField(max_length=128)
    diagnosed_at = models.DateTimeField()
    medication_name = models.CharField(max_length=128, null=True, blank=True)
    milk_withdrawal_days = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
