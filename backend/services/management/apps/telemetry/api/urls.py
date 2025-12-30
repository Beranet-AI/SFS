# apps/telemetry/api/urls.py

from django.urls import path
from .edge_controller import EdgeControllerTelemetryView
from .commands import CommandResultTelemetryView

urlpatterns = [
    path(
        "edge/",
        EdgeControllerTelemetryView.as_view(),
        name="telemetry",
    ),
    path(
        "commands/",
        CommandResultTelemetryView.as_view(),
        name="command-result",
    ),
]
