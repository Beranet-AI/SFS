from django.db import models
from apps.farms.domain.value_objects.barn_type import BarnType


class FarmModel(models.Model):
    name = models.CharField(max_length=255)

    # Location (ValueObject flattened)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "farms_farmmodel"

    def __str__(self):
        return self.name


class BarnModel(models.Model):
    farm = models.ForeignKey(
        FarmModel,
        on_delete=models.CASCADE,
        related_name="barns",
    )

    name = models.CharField(max_length=255)

    barn_type = models.CharField(
        max_length=32,
        choices=BarnType.choices(),
        default=BarnType.FREE_STALL,
    )

    capacity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "farms_barnmodel"

    def __str__(self):
        return f"{self.name} ({self.farm.name})"


class ZoneModel(models.Model):
    barn = models.ForeignKey(
        BarnModel,
        on_delete=models.CASCADE,
        related_name="zones",
    )

    name = models.CharField(max_length=255)
    purpose = models.CharField(max_length=64)

    class Meta:
        db_table = "farms_zonemodel"

    def __str__(self):
        return f"{self.name} ({self.barn.name})"


class ZoneEnvironmentHistoryModel(models.Model):
    """
    تاریخچه محیط برای AI / تحلیل روند
    """
    zone = models.ForeignKey(
        ZoneModel,
        on_delete=models.CASCADE,
        related_name="history",
    )
    temperature_c = models.FloatField()
    humidity = models.FloatField()
    ammonia_ppm = models.FloatField()
    co2_ppm = models.FloatField(null=True, blank=True)
    airflow_mps = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "farms_zone_environment_history"
