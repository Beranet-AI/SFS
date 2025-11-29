from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Animal, RfidTag


@admin.register(RfidTag)
class RfidTagAdmin(admin.ModelAdmin):
    list_display = ("id", "tag_code", "farm", "status", "updated_at")
    list_filter = ("status", "farm")
    search_fields = ("tag_code",)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("id", "species", "farm", "barn", "current_zone", "rfid_tag", "status")
    list_filter = ("species", "status", "farm", "barn")
    search_fields = ("external_id", "notes")
