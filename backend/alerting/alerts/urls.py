from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActiveAlertsView, AlertRuleViewSet, AlertViewSet


router = DefaultRouter()
router.register(r"alert-rules", AlertRuleViewSet, basename="alert-rule")
router.register(r"alerts", AlertViewSet, basename="alert")


urlpatterns = [
    path("", include(router.urls)),
    path("alerts/active/", ActiveAlertsView.as_view(), name="alerts-active"),
]
