from django.contrib import admin
from ..models.models import FarmModel
from .barn_admin import BarnInline


@admin.register(FarmModel)
class FarmAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "city",
        "barn_count",
        "created_at",
    )

    search_fields = (
        "name",
        "country",
        "city",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = [
        BarnInline,
    ]

    @admin.display(description="Barns")
    def barn_count(self, obj):
        return obj.barns.count()
