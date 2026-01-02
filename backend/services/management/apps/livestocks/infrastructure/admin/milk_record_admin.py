from django.contrib import admin
from ..models.models import MilkRecordModel


class MilkRecordInline(admin.TabularInline):
    model = MilkRecordModel
    extra = 0
    can_delete = False

    readonly_fields = (
        "amount_liters",
        "recorded_at",
    )

    def has_add_permission(self, request, obj):
        return False
