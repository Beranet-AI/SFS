# File: farm/infrastructure/admin/farm_admin.py
from django.contrib import admin
from ..models import FarmModel

@admin.register(FarmModel)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "city")
