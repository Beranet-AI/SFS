# File: livestock/api/urls.py
from django.urls import path
from .views import (
    RegisterLivestockView,
    RecordHealthMetricsView,
    RecordNutritionMetricsView,
    RecordMilkProductionView,
    RecordReproductionView,
    RecordTreatmentView,
    LivestockAIInsightsView,
)

urlpatterns = [
    path("livestock/", RegisterLivestockView.as_view()),
    path("livestock/<str:livestock_id>/health/", RecordHealthMetricsView.as_view()),
    path("livestock/<str:livestock_id>/nutrition/", RecordNutritionMetricsView.as_view()),
    path("livestock/<str:livestock_id>/milk/", RecordMilkProductionView.as_view()),
    path("livestock/<str:livestock_id>/reproduction/", RecordReproductionView.as_view()),
    path("livestock/<str:livestock_id>/treatment/", RecordTreatmentView.as_view()),
    path("livestock/<str:livestock_id>/ai-insights/", LivestockAIInsightsView.as_view()),
]
