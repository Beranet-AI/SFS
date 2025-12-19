from django.contrib import admin
from .infrastructure.models.farm_model import FarmModel

@admin.register(FarmModel)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
