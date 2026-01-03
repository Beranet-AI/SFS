from django.urls import path
from apps.commands.api.edge_controller import (
    CommandCreateController,
    CommandDetailController,
    CommandAckController,
    CommandResultController,
)

urlpatterns = [
    path("commands/", CommandCreateController.as_view(), name="command-create"),
    path(
        "commands/<uuid:command_id>/",
        CommandDetailController.as_view(),
        name="command-detail",
    ),
    path("commands/ack/", CommandAckController.as_view(), name="command-ack"),
    path("commands/result/", CommandResultController.as_view(), name="command-result"),
]
