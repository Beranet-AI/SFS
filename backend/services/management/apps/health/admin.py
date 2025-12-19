from django.contrib import admin
from .infrastructure.models.medical_record_model import MedicalRecordModel

@admin.register(MedicalRecordModel)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "livestock_id", "diagnosis", "recorded_at")
    list_filter = ("diagnosis",)
