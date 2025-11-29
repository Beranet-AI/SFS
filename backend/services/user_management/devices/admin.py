from django.contrib import admin

# Register your models here.

from .models import Device, SensorType, Sensor


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "farm", "barn", "zone", "status", "last_seen_at", "is_active")
    list_filter = ("type", "status", "farm", "barn", "zone", "is_active")
    search_fields = ("name", "serial_number", "ip_address")


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "unit", "min_value", "max_value")
    search_fields = ("name", "code")


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sensor_type", "device", "is_active")
    list_filter = ("sensor_type", "is_active")
    search_fields = ("name", "hardware_address")
