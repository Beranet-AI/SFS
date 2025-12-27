from django.contrib import admin
from apps.devices.models import DeviceModel


@admin.register(DeviceModel)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "kind",
        "display_name",
        "status",
        "farm_id",
        "livestock_id",
        "updated_at",
    )

    list_filter = (
        "kind",
        "status",
        "farm_id",
    )

    search_fields = (
        "display_name",
        "id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
