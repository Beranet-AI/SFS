from django.urls import include, path
from rest_framework.routers import DefaultRouter

import importlib

from devices.views import DeviceViewSet, SensorTypeViewSet, SensorViewSet
from farm.views import BarnViewSet, FarmHierarchyView, FarmViewSet, ZoneViewSet
from telemetry.views import HistoricalReadingsView, LatestReadingsView, SensorReadingViewSet


def _register_alert_routes(router: DefaultRouter) -> None:
    """Register alerting routes only when the alerting package is installed."""

    spec = importlib.util.find_spec("alerting.alerts.views")
    if spec is None:
        return

    alert_views = importlib.import_module("alerting.alerts.views")
    router.register(
        r"alert-rules",
        getattr(alert_views, "AlertRuleViewSet"),
        basename="alert-rule",
    )
    router.register(
        r"alerts",
        getattr(alert_views, "AlertViewSet"),
        basename="alert",
    )
    router.register(
        r"active-alerts",
        getattr(alert_views, "ActiveAlertsView"),
        basename="active-alert",
    )
router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"sensor-types", SensorTypeViewSet, basename="sensor-type")
router.register(r"sensors", SensorViewSet, basename="sensor")
router.register(r"sensor-readings", SensorReadingViewSet, basename="sensor-reading")
router.register(r"farms", FarmViewSet, basename="farm")
router.register(r"barns", BarnViewSet, basename="barn")
router.register(r"zones", ZoneViewSet, basename="zone")

_register_alert_routes(router)
urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/latest-readings/", LatestReadingsView.as_view(), name="latest-readings"),
    path("dashboard/historical-readings/", HistoricalReadingsView.as_view(), name="historical-readings"),
    path("dashboard/farm-hierarchy/", FarmHierarchyView.as_view(), name="farm-hierarchy"),
]
