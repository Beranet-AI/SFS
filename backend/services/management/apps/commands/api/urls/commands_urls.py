from django.urls import path

from apps.commands.api.views.ack_command_view import AckCommandView
from apps.commands.api.views.actions.send_command_view import SendCommandView
from apps.commands.api.views.get_command_view import GetCommandView
from apps.commands.api.views.receive_result_view import ReceiveResultView

urlpatterns = [
    path("", SendCommandView.as_view(), name="command-send"),
    path("<uuid:command_id>/", GetCommandView.as_view(), name="command-get"),
    path("ack/", AckCommandView.as_view(), name="command-ack"),
    path("result/", ReceiveResultView.as_view(), name="command-result"),
]
