urlpatterns = [
    path("api/v1/events/", include("apps.events.api.urls")),
    path("api/v1/telemetry/", include("apps.telemetry.api.urls")),
    path("api/v1/livestock/", include("apps.livestock.api.urls")),
    path("api/v1/farms/", include("apps.farms.api.urls")),
    path("api/v1/users/", include("apps.users.api.urls")),
    
]
