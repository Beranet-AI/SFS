from django.urls import path
from apps.commands.api.views import (
    CommandCreateView,
    CommandDetailView,
    CommandAckView,
    CommandResultView,
)

urlpatterns = [
    path("commands/", CommandCreateView.as_view(), name="command-create"),
    path("commands/<uuid:command_id>/", CommandDetailView.as_view(), name="command-detail"),
    path("commands/ack/", CommandAckView.as_view(), name="command-ack"),
    path("commands/result/", CommandResultView.as_view(), name="command-result"),
]
