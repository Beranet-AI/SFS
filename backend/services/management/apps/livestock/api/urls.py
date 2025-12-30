from django.urls import path
from .views import (
    LivestockView,
    LivestockHealthEvalView,
    LivestockSensorGroupView,
)

urlpatterns = [
    path("", LivestockView.as_view()),
    path("<str:livestock_id>/evaluate-health/", LivestockHealthEvalView.as_view()),
    path("sensor-groups/", LivestockSensorGroupView.as_view()),
]
