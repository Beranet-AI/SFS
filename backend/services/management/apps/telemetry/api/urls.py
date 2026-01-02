# backend/services/management/apps/telemetry/api/urls.py
# backend/services/management/apps/telemetry/api/urls.py

from django.urls import path
from .views import ApproveTelemetrySchemaView
from .edge_controller import EdgeControllerTelemetryView
from .data_ingestion import DataIngestionValidationView

urlpatterns = [
    path(
        "schemas/<uuid:schema_id>/approve/",
        ApproveTelemetrySchemaView.as_view(),
        name="telemetry-approve-schema",
    ),
    path(
        "edge-controller/telemetry/",
        EdgeControllerTelemetryView.as_view(),
        name="telemetry-edge-controller",
    ),
    path(
        "data-ingestion/validation/",
        DataIngestionValidationView.as_view(),
        name="telemetry-data-ingestion-validation",
    ),
]
