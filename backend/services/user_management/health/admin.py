from django.contrib import admin

from .models import Cow, Disease, DiseaseRecord, MLModel, Prediction, SensorData


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
