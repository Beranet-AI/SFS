# File: farm/infrastructure/admin/zone_admin.py
from django.contrib import admin
from ..models import ZoneModel

@admin.register(ZoneModel)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "barn", "temperature_c", "humidity", "ammonia_ppm", "co2_ppm", "airflow_mps", "updated_at")
    readonly_fields = ("updated_at",)
