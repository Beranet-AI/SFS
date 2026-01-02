from django.contrib import admin
from ..models.models import HealthRecordModel


class HealthRecordInline(admin.TabularInline):
    model = HealthRecordModel
    extra = 0
    can_delete = False

    readonly_fields = (
        "status",
        "temperature",
        "recorded_at",
    )

    def has_add_permission(self, request, obj):
        return False
