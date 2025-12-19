from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/", include([
        path("users/", include("apps.users.api.urls")),
        path("farms/", include("apps.farms.api.urls")),
        path("livestock/", include("apps.livestock.api.urls")),
        path("devices/", include("apps.devices.api.urls")),
        path("telemetry/", include("apps.telemetry.api.urls")),
        path("health/", include("apps.health.api.urls")),
        path("incidents/", include("apps.incidents.api.urls")),
        path("rules/", include("apps.rules.api.urls")),
        path("integrations/", include("apps.integrations.api.urls")),
    ])),
]
