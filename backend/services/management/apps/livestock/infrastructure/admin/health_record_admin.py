# File: livestock/infrastructure/admin/health_record_admin.py
from django.contrib import admin
from ..models import HealthRecordModel

@admin.register(HealthRecordModel)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "livestock", "temperature_c", "activity", "rumination_minutes", "recorded_at")
    list_filter = ("livestock",)
    readonly_fields = ("recorded_at",)
