from django.urls import path
from .views import TelemetryIngestView, TelemetryRecentView

urlpatterns = [
    path("ingest/", TelemetryIngestView.as_view()),
    path("recent/<str:livestock_id>/", TelemetryRecentView.as_view()),
]
