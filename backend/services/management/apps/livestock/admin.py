from django.contrib import admin
from .infrastructure.models.livestock_model import LivestockModel

@admin.register(LivestockModel)
class LivestockAdmin(admin.ModelAdmin):
    list_display = ("id", "tag", "farm_id", "barn", "zone", "health_state")
