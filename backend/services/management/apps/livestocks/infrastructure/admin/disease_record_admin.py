from django.contrib import admin
from ..models.models import DiseaseRecordModel


class DiseaseRecordInline(admin.TabularInline):
    model = DiseaseRecordModel
    extra = 0
    can_delete = False

    readonly_fields = (
        "disease_name",
        "severity",
        "detected_at",
    )

    def has_add_permission(self, request, obj):
        return False
