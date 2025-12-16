from django.contrib import admin

from .models import LiveStatus, LiveStatusRule


@admin.register(LiveStatusRule)
class LiveStatusRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "farm", "severity", "is_active", "updated_at")
    list_filter = ("farm", "severity", "is_active")
    search_fields = ("name", "description", "condition_expression")


@admin.register(LiveStatus)
class LiveStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "severity", "state", "farm", "barn", "zone", "sensor", "animal", "raised_at")
    list_filter = ("severity", "state", "farm", "barn")
    search_fields = ("message",)
    date_hierarchy = "raised_at"
