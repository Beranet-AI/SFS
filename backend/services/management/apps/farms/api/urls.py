# farm/api/urls.py
from django.urls import path
from .views import RecordZoneEnvironmentView

urlpatterns = [
    path(
        "farms/<str:farm_id>/barn/<str:barn_id>/zone/<str:zone_id>/environment/",
        RecordZoneEnvironmentView.as_view()
    ),
]
