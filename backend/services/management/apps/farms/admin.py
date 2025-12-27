from django.contrib import admin
from .models import FarmModel


@admin.register(FarmModel)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
