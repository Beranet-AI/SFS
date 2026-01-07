from django.urls import path

from apps.commands.api.views import receive_command_result_view

urlpatterns = [
    path("results/", receive_command_result_view, name="commands_receive_result_api"),
]
