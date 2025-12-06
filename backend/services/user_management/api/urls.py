from django.urls import path, include
from rest_framework.routers import DefaultRouter
from telemetry.views import SensorReadingViewSet, LatestReadingsView, HistoricalReadingsView
from devices.views import DeviceViewSet, SensorTypeViewSet, SensorViewSet
from farm.views import FarmViewSet, BarnViewSet, ZoneViewSet, FarmHierarchyView



router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"sensor-types", SensorTypeViewSet, basename="sensor-type")
router.register(r"sensors", SensorViewSet, basename="sensor")
router.register(r"sensor-readings", SensorReadingViewSet, basename="sensor-reading")
router.register(r"farms", FarmViewSet, basename="farm")
router.register(r"barns", BarnViewSet, basename="barn")
router.register(r"zones", ZoneViewSet, basename="zone")


urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/latest-readings/", LatestReadingsView.as_view(), name="latest-readings"),
    path("dashboard/historical-readings/", HistoricalReadingsView.as_view(), name="historical-readings"),  # ✅ جدید
    path("dashboard/farm-hierarchy/", FarmHierarchyView.as_view(), name="farm-hierarchy"),
]
