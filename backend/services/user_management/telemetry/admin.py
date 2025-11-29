from django.contrib import admin

# Register your models here.

from .models import SensorReading


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ("id", "sensor", "ts", "value", "quality")
    list_filter = ("quality", "sensor__sensor_type", "sensor__device__farm")
    search_fields = ("sensor__name",)
    date_hierarchy = "ts"
