from django.contrib import admin
from .models import LivestockModel, LivestockSensorGroupModel


@admin.register(LivestockModel)
class LivestockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "farm_id",
        "barn",
        "zone",
        "health_state",
    )


@admin.register(LivestockSensorGroupModel)
class LivestockSensorGroupAdmin(admin.ModelAdmin):
    list_display = (
        "livestock",
        "rfid_device",
        "updated_at",
    )
