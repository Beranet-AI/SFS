# File: farm/infrastructure/admin/barn_admin.py
from django.contrib import admin
from ..models import BarnModel

@admin.register(BarnModel)
class BarnAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "farm")
