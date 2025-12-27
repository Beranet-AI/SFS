from django.contrib import admin
from .models import IncidentModel


@admin.register(IncidentModel)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "severity",
        "status",
        "source",
        "device_id",
        "occurred_at",
    )
    list_filter = ("severity", "status", "source")
    search_fields = ("title", "description", "device_id")
    ordering = ("-occurred_at",)
