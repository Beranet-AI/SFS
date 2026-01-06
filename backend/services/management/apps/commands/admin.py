from django.contrib import admin
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
from apps.commands.infrastructure.models.command_execution_model import (
    CommandAttemptModel,
)
from apps.commands.infrastructure.models.command_model import CommandModel


@admin.register(CommandModel)
class CommandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "command_name",
        "target_kind",
        "target_id",
        "edge_node_id",
        "status",
        "created_at",
    )

    list_filter = ("status", "target_kind", "command_name")
    search_fields = ("id", "target_id", "edge_node_id", "idempotency_key")

    readonly_fields = (
        "id",
        "created_at",
        "acked_at",
        "started_at",
        "finished_at",
    )

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(
                "send-command/",
                self.admin_site.admin_view(send_command_view),
                name="commands_commandmodel_send",
            ),
            path(
                "send/",
                self.admin_site.admin_view(send_command_view),
                name="commands_commandmodel_send_legacy",
            ),
            path(
                "receive-result/",
                self.admin_site.admin_view(scan_result_view),
                name="commands_commandmodel_receive_result",
            ),
            path(
                "dashboard/",
                self.admin_site.admin_view(command_dashboard_view),
                name="commands_commandmodel_dashboard",
            ),
            path(
                "discover/",
                self.admin_site.admin_view(discover_view),
                name="commands_discover",
            ),
        ] + urls


@admin.register(CommandAttemptModel)
class CommandExecutionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "command",
        "attempt_no",
        "status",
        "created_at",
        "dispatched_at",
        "acked_at",
        "result_at",
    )
    list_filter = ("status",)
    search_fields = ("id", "command__id", "executor_receipt")
    readonly_fields = ("id", "created_at")
