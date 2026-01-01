# File: livestock/infrastructure/admin/livestock_admin.py
from django.contrib import admin
from ..models import LivestockModel

@admin.register(LivestockModel)
class LivestockAdmin(admin.ModelAdmin):
    list_display = ("id", "tag_id", "breed", "sex", "status", "updated_at")
    search_fields = ("tag_id", "breed")
    list_filter = ("sex", "status")
    readonly_fields = ("created_at", "updated_at")
