from django.contrib import admin

# Register your models here.

from .models import Farm, Barn, Zone


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "location", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "code", "location")


@admin.register(Barn)
class BarnAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "farm", "code", "is_active")
    list_filter = ("farm", "is_active")
    search_fields = ("name", "code")


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "barn", "is_active")
    list_filter = ("barn", "is_active")
    search_fields = ("name", "code")
