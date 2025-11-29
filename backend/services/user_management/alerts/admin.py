from django.contrib import admin

# Register your models here.

from .models import AlertRule, Alert


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "farm", "scope", "severity", "is_active", "updated_at")
    list_filter = ("farm", "scope", "severity", "is_active")
    search_fields = ("name", "description", "condition_expression")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "severity", "status", "farm", "barn", "zone", "sensor", "animal", "raised_at")
    list_filter = ("severity", "status", "farm", "barn")
    search_fields = ("message",)
    date_hierarchy = "raised_at"
