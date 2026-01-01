# farm/infrastructure/models.py
from django.db import models


class FarmModel(models.Model):
    name = models.CharField(max_length=255)

    country = models.CharField(max_length=64, blank=True, default="")
    city = models.CharField(max_length=64, blank=True, default="")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    feed_cost = models.FloatField(null=True, blank=True)
    treatment_cost = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BarnModel(models.Model):
    farm = models.ForeignKey(FarmModel, on_delete=models.CASCADE, related_name="barns")
    name = models.CharField(max_length=255)


class ZoneModel(models.Model):
    barn = models.ForeignKey(BarnModel, on_delete=models.CASCADE, related_name="zones")
    name = models.CharField(max_length=255)

    temperature_c = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    ammonia_ppm = models.FloatField(null=True, blank=True)
    co2_ppm = models.FloatField(null=True, blank=True)
    airflow_mps = models.FloatField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)


class ZoneEnvironmentHistoryModel(models.Model):
    """
    اختیاری ولی حرفه‌ای:
    تاریخچه محیط برای AI / تحلیل روند
    """
    zone = models.ForeignKey(ZoneModel, on_delete=models.CASCADE, related_name="history")
    temperature_c = models.FloatField()
    humidity = models.FloatField()
    ammonia_ppm = models.FloatField()
    co2_ppm = models.FloatField(null=True, blank=True)
    airflow_mps = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
