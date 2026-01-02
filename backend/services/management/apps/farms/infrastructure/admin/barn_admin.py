from django.contrib import admin
from ..models.models import BarnModel
from .zone_admin import ZoneInline


class BarnInline(admin.TabularInline):
    model = BarnModel
    extra = 0
    show_change_link = True

    fields = (
        "name",
        "barn_type",
        "zone_count",
    )

    readonly_fields = (
        "zone_count",
    )

    inlines = [
        ZoneInline,
    ]

    @admin.display(description="Zones")
    def zone_count(self, obj):
        return obj.zones.count()
