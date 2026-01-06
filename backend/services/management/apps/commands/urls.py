from django.urls import path

from apps.commands.api.admin_views.command_dashboard import (
    command_dashboard_view,
)
from apps.commands.api.admin_views.discover_view import (
    discover_view,
)
from apps.commands.api.admin_views.scan_result_view import (
    scan_result_view,
)
from apps.commands.api.admin_views.send_command_view import (
    send_command_view,
)

urlpatterns = [
    path("admin/commands/send/", send_command_view, name="commands_send"),
    path(
        "admin/commands/receive-result/",
        scan_result_view,
        name="commands_receive_result",
    ),
    path(
        "admin/commands/dashboard/",
        command_dashboard_view,
        name="commands_dashboard",
    ),
    path(
        "admin/commands/discover/",
        discover_view,
        name="commands_discover",
    ),
]
