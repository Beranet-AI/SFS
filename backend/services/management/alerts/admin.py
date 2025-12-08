from django.contrib import admin

from alerts.models import AlertLog, AlertRule


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "sensor", "operator", "threshold_value", "enabled", "created_at")
    list_filter = ("enabled", "operator", "sensor__sensor_type__code")
    search_fields = ("sensor__name", "sensor__sensor_type__code")
    autocomplete_fields = ("sensor",)


@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = ("id", "sensor", "value", "triggered_at", "alert_rule")
    list_filter = ("sensor__sensor_type__code",)
    search_fields = ("sensor__name",)
    autocomplete_fields = ("sensor", "alert_rule")
    readonly_fields = ("triggered_at", "value")
