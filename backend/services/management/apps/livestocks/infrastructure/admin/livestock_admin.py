from django.contrib import admin
from ..models.models import LivestockModel
from .health_record_admin import HealthRecordInline
from .milk_record_admin import MilkRecordInline
from .disease_record_admin import DiseaseRecordInline


@admin.register(LivestockModel)
class LivestockAdmin(admin.ModelAdmin):
    list_display = (
        "tag_id",
        "species",
        "breed",
        "farm",
        "latest_health_status",
        "latest_temperature",
        "latest_milk_amount",
        "birth_date",
    )

    list_filter = (
        "species",
        "breed",
        "farm",
    )

    search_fields = (
        "tag_id",
    )

    readonly_fields = (
        "tag_id",
        "species",
        "breed",
        "farm",
        "birth_date",
        "created_at",
        "latest_health_status",
        "latest_temperature",
        "latest_milk_amount",
    )

    inlines = [
        HealthRecordInline,
        MilkRecordInline,
        DiseaseRecordInline,
    ]

    # =========================
    # Derived / ValueObject-like
    # =========================

    @admin.display(description="Health Status")
    def latest_health_status(self, obj):
        record = obj.health_records.order_by("-recorded_at").first()
        return record.status if record else "—"

    @admin.display(description="Temperature (°C)")
    def latest_temperature(self, obj):
        record = obj.health_records.order_by("-recorded_at").first()
        return record.temperature if record else "—"

    @admin.display(description="Milk (L)")
    def latest_milk_amount(self, obj):
        record = obj.milk_records.order_by("-recorded_at").first()
        return record.amount_liters if record else "—"
