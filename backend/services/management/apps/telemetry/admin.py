from django.contrib import admin
from .models import TelemetryModel


@admin.register(TelemetryModel)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device_id",
        "livestock_id",
        "metric",
        "value",
        "recorded_at",
    )
    list_filter = ("metric",)
    search_fields = ("device_id", "livestock_id", "metric")
