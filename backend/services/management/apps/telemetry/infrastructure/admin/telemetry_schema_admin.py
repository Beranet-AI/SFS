from django.contrib import admin
from ..models import TelemetrySchemaModel


@admin.register(TelemetrySchemaModel)
class TelemetrySchemaAdmin(admin.ModelAdmin):
    """
    Telemetry schema registry (governance only)
    """

    list_display = (
        "name",
        "version",
        "approved",
        "created_at",
    )

    list_filter = (
        "approved",
    )

    search_fields = (
        "name",
        "version",
    )

    readonly_fields = (
        "name",
        "version",
        "schema",
        "created_at",
    )

    actions = ["approve_schema"]

    def approve_schema(self, request, queryset):
        queryset.update(approved=True)

    approve_schema.short_description = "Approve selected schemas"
