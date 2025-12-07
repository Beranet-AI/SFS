from django.contrib import admin

from .models import (
    ClinicalEvent,
    Cow,
    Disease,
    DiseaseRecord,
    LabResult,
    ManagementEvent,
    MLModel,
    Prediction,
    SensorData,
    TreatmentLog,
)


@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ("id", "animal", "lactation_stage", "parity", "days_in_milk")
    search_fields = ("animal__id", "animal__external_id")
    list_filter = ("lactation_stage",)


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "framework", "disease", "is_active")
    list_filter = ("framework", "is_active")
    search_fields = ("name", "version")


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ("sensor", "cow", "ts", "value", "quality")
    list_filter = ("quality",)
    search_fields = ("sensor__name", "cow__animal__id")


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("disease", "cow", "status", "probability", "predicted_at")
    list_filter = ("status", "disease")
    search_fields = ("cow__animal__id",)


@admin.register(DiseaseRecord)
class DiseaseRecordAdmin(admin.ModelAdmin):
    list_display = ("disease", "cow", "status", "diagnosed_at", "resolved_at")
    list_filter = ("status", "disease")
    search_fields = ("cow__animal__id",)


@admin.register(ClinicalEvent)
class ClinicalEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "cow", "disease", "occurred_at", "severity")
    list_filter = ("event_type", "disease")
    search_fields = ("cow__animal__id", "symptom")


@admin.register(TreatmentLog)
class TreatmentLogAdmin(admin.ModelAdmin):
    list_display = ("treatment_type", "cow", "disease", "started_at", "completed_at")
    list_filter = ("treatment_type", "disease")
    search_fields = ("cow__animal__id", "medication")


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ("parameter", "value", "unit", "cow", "result_at")
    list_filter = ("parameter", "disease")
    search_fields = ("cow__animal__id",)


@admin.register(ManagementEvent)
class ManagementEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "cow", "occurred_at")
    list_filter = ("event_type",)
    search_fields = ("cow__animal__id",)
