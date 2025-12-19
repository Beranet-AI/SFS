from django.contrib import admin
from .infrastructure.models.incident_model import IncidentModel

@admin.register(IncidentModel)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "livestock_id",
        "severity",
        "status",
        "source",
        "created_at",
    )
    list_filter = ("severity", "status", "source")
