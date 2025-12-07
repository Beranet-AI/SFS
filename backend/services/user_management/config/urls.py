from django.contrib import admin
from django.urls import path, include
from api import views

# Import ActiveAlertsView directly to guarantee the endpoint is always routable
from alerting.alerts.views import ActiveAlertsView


urlpatterns = [
    path("admin/", admin.site.urls),
    # Explicit top-level mapping so /api/v1/alerts/active/ never 404s
    path("api/v1/alerts/active/", ActiveAlertsView.as_view(), name="alert-active-root"),
    path("api/v1/", include("api.urls")),
]
