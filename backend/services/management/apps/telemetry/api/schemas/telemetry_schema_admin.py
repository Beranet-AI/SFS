# backend/services/management/apps/telemetry/api/schemas/telemetry_schema_admin.py

from django.contrib import admin
from django.utils.html import format_html


from ..infrastructure.models.telemetry_schema import TelemetrySchema


@admin.register(TelemetrySchema)
class TelemetrySchemaAdmin(admin.ModelAdmin):
    """
    Admin UI for TelemetrySchemaRegistry
    """

    list_display = (
        "device_type",
        "version",
        "is_active",
        "created_by",
        "approved_by",
        "created_at",
    )

    list_filter = (
        "device_type",
        "is_active",
        "created_at",
    )

    search_fields = (
        "device_type",
        "version",
    )

    ordering = ("device_type", "-created_at")

    readonly_fields = (
        "id",
        "version",
        "approved_at",
        "created_at",
    )

    fieldsets = (
        (
            "Schema Identity",
            {
                "fields": (
                    "id",
                    "device_type",
                    "version",
                    "is_active",
                )
            },
        ),
        (
            "Schema Definition",
            {
                "fields": (
                    "json_schema",
                    "raw_example",
                )
            },
        ),
        (
            "Audit",
            {
                "field
