# backend/services/user_management/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter


from farm.views import FarmViewSet, BarnViewSet, ZoneViewSet
from devices.views import DeviceViewSet, SensorTypeViewSet, SensorViewSet
from telemetry.views import SensorReadingViewSet, LatestReadingsView
from livestock.views import AnimalViewSet, RfidTagViewSet
from alerts.views import AlertRuleViewSet, AlertViewSet




router = DefaultRouter()
router.register(r"farms", FarmViewSet, basename="farm")
router.register(r"barns", BarnViewSet, basename="barn")
router.register(r"zones", ZoneViewSet, basename="zone")

router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"sensor-types", SensorTypeViewSet, basename="sensor-type")
router.register(r"sensors", SensorViewSet, basename="sensor")

router.register(r"sensor-readings", SensorReadingViewSet, basename="sensor-reading")

router.register(r"rfid-tags", RfidTagViewSet, basename="rfid-tag")
router.register(r"animals", AnimalViewSet, basename="animal")

router.register(r"alert-rules", AlertRuleViewSet, basename="alert-rule")
router.register(r"alerts", AlertViewSet, basename="alert")

urlpatterns = [
    # main REST API
    path("", include(router.urls)),
    path("dashboard/latest-readings/", LatestReadingsView.as_view(), name="latest-readings"),
]


