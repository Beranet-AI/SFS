from django.urls import path, include
from rest_framework.routers import DefaultRouter
from telemetry.views import SensorReadingViewSet, LatestReadingsView, HistoricalReadingsView



router = DefaultRouter()
router.register(r"sensor-readings", SensorReadingViewSet, basename="sensor-reading")


urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/latest-readings/", LatestReadingsView.as_view(), name="latest-readings"),
    path("dashboard/historical-readings/", HistoricalReadingsView.as_view(), name="historical-readings"),  # ✅ جدید
]
