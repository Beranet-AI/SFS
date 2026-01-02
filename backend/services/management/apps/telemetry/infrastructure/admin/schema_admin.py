from django.contrib import admin
from ..models import TelemetrySchemaModel


@admin.register(TelemetrySchemaModel)
class SchemaAdmin(admin.ModelAdmin):
    """
    Telemetry schema registry (governance only)
    """

    list_display = (
        "device_type",
        "version",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "device_type",
        "version",
    )

    readonly_fields = (
        "device_type",
        "version",
        "created_at",
        "approved_at",
    )

    actions = ["activate_schema"]

    def activate_schema(self, request, queryset):
        queryset.update(is_active=True)

    activate_schema.short_description = "Activate selected schemas"
