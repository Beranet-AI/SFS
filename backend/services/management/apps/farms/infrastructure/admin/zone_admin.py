from django.contrib import admin
from ..models.models import ZoneModel, ZoneEnvironmentHistoryModel


class ZoneEnvironmentInline(admin.TabularInline):
    model = ZoneEnvironmentHistoryModel
    extra = 0
    can_delete = False
    max_num = 0

    fields = (
        "temperature",
        "humidity",
        "ammonia",
        "recorded_at",
    )

    readonly_fields = fields


class ZoneInline(admin.StackedInline):
    model = ZoneModel
    extra = 0
    show_change_link = True

    fields = (
        "name",
        "zone_type",
        "capacity",
    )

    inlines = [
        ZoneEnvironmentInline,
    ]
