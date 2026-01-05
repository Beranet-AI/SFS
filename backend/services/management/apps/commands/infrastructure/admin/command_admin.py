from django.contrib import admin
from django.urls import path

from apps.commands.infrastructure.admin.views import (
    command_dashboard_view,
    load_command_detail,
    receive_result_view,
    send_command_view,
)
from apps.commands.infrastructure.models.command_attempt_model import (
    CommandAttemptModel,
)
from apps.commands.infrastructure.models.command_model import CommandModel


@admin.register(CommandModel)
class CommandAdmin(admin.ModelAdmin):
    change_list_template = "admin/commands/commandmodel/change_list.html"

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

    actions = ["load_command_details"]

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(
                "send/",
                self.admin_site.admin_view(send_command_view),
                name="commands_commandmodel_send",
            ),
            path(
                "receive-result/",
                self.admin_site.admin_view(receive_result_view),
                name="commands_commandmodel_receive_result",
            ),
            path(
                "dashboard/",
                self.admin_site.admin_view(command_dashboard_view),
                name="commands_commandmodel_dashboard",
            ),
        ] + urls

    def load_command_details(self, request, queryset):
        command = load_command_detail(request, queryset)
        if command:
            self.message_user(
                request,
                f"Loaded command {command.id} ({command.command_name}).",
            )

    load_command_details.short_description = "Load command details (use case)"


@admin.register(CommandAttemptModel)
class CommandAttemptAdmin(admin.ModelAdmin):
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
