from django.contrib import admin
from django.utils.html import format_html

from ..models import TelemetryRecordModel


@admin.register(TelemetryRecordModel)
class TelemetryRecordAdmin(admin.ModelAdmin):
    """
    Read-only telemetry viewer (industrial-grade)
    """

    list_display = (
        "recorded_at",
        "metric",
        "value_preview",
        "unit",
        "source",
        "farm",
        "barn",
        "zone",
        "livestock",
    )

    list_filter = (
        "metric",
        "source",
        "farm",
        "barn",
        "zone",
        "livestock",
        ("recorded_at", admin.DateFieldListFilter),
    )

    search_fields = (
        "metric",
        "farm__name",
        "barn__name",
        "zone__name",
        "livestock__tag_id",
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
        "farm",
        "barn",
        "zone",
        "livestock",
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
                "farm",
                "barn",
                "zone",
                "livestock",
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
