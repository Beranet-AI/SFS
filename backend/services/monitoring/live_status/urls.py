from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActiveLiveStatusView, LiveStatusRuleViewSet, LiveStatusViewSet

router = DefaultRouter()
router.register(r"live-status/rules", LiveStatusRuleViewSet, basename="live-status-rule")
router.register(r"live-status", LiveStatusViewSet, basename="live-status")

urlpatterns = [
    path("", include(router.urls)),
    path("live-status/active/", ActiveLiveStatusView.as_view(), name="live-status-active"),
]
