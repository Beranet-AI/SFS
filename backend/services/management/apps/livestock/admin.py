from django.contrib import admin
from .models import LivestockModel


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
