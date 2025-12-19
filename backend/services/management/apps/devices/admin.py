from django.contrib import admin
from .infrastructure.models.device_model import DeviceModel

@admin.register(DeviceModel)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "serial", "device_type", "status", "assigned_livestock_id")
    list_filter = ("device_type", "status")
