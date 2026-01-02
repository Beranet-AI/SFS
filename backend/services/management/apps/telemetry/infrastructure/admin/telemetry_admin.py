from django.contrib import admin

from ..models import TelemetryModel


@admin.register(TelemetryModel)
class TelemetryAdmin(admin.ModelAdmin):
    """
    Read-only telemetry viewer (industrial-grade)
    """

    list_display = (
        "recorded_at",
        "metric",
        "value_preview",
        "unit",
        "source",
        "farm_id",
        "barn_id",
        "zone_id",
        "livestock_id",
    )

    list_filter = (
        "metric",
        "source",
        "farm_id",
        "barn_id",
        "zone_id",
        "livestock_id",
        ("recorded_at", admin.DateFieldListFilter),
    )

    search_fields = (
        "metric",
        "farm_id",
        "barn_id",
        "zone_id",
        "livestock_id",
    )

    ordering = ("-recorded_at",)

    date_hierarchy = "recorded_at"

    list_per_page = 50
    list_max_show_all = 200

    readonly_fields = (
        "metric",
        "value",
        "unit",
        "source",
        "payload",
        "recorded_at",
        "farm_id",
        "barn_id",
        "zone_id",
        "livestock_id",
    )

    fieldsets = (
        ("Telemetry Info", {
            "fields": (
                "metric",
                "value",
                "unit",
                "source",
                "recorded_at",
            )
        }),
        ("Context", {
            "fields": (
                "farm_id",
                "barn_id",
                "zone_id",
                "livestock_id",
            )
        }),
        ("Raw Payload (JSON)", {
            "classes": ("collapse",),
            "fields": ("payload",),
        }),
    )

    # 🔒 Disable mutations
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description="Value")
    def value_preview(self, obj):
        if isinstance(obj.value, (int, float)):
            return f"{obj.value:.2f}"
        return str(obj.value)
