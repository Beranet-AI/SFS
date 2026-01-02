# backend/services/management/apps/telemetry/api/urls.py
# backend/services/management/apps/telemetry/api/urls.py

from django.urls import path
from .views import ApproveTelemetrySchemaView

urlpatterns = [
    path(
        "schemas/<uuid:schema_id>/approve/",
        ApproveTelemetrySchemaView.as_view(),
        name="telemetry-approve-schema",
    ),
]
