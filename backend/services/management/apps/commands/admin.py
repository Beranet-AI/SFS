from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, reverse

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

from apps.commands.infrastructure.models.command_model import CommandModel
from apps.commands.infrastructure.models.command_execution_model import (
    CommandAttemptModel,
)
from apps.commands.infrastructure.models.network_scan_result_model import (
    NetworkScanResultModel,
)




# =========================================================
# Command Admin (Commands lifecycle & actions)
# =========================================================

@admin.register(CommandModel)
class CommandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "command_name",
        "target_kind",
        "target_id",
        "status",
        "created_at",
    )

    list_filter = ("status", "target_kind", "command_name")
    search_fields = ("id", "target_id", "idempotency_key")

    readonly_fields = (
        "id",
        "created_at",
        "acked_at",
        "started_at",
        "finished_at",
    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            # Command actions
            path(
                "send/",
                self.admin_site.admin_view(send_command_view),
                name="commands_send",
            ),
            path(
                "receive-result/",
                self.admin_site.admin_view(scan_result_view),
                name="commands_receive_result",
            ),

            # Dashboards
            path(
                "dashboard/",
                self.admin_site.admin_view(command_dashboard_view),
                name="commands_dashboard",
            ),

            # Discover (Admin View مستقل)
            path(
                "discover/",
                self.admin_site.admin_view(discover_view),
                name="commands_discover",
            ),
        ]

        # ⚠️ ترتیب حیاتی است
        return custom_urls + urls


# =========================================================
# Command Attempts (Execution history)
# =========================================================

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


# =========================================================
# Discover / Network Scan Results (Read-only, redirected)
# =========================================================

@admin.register(NetworkScanResultModel)
class NetworkScanResultAdmin(admin.ModelAdmin):
    list_display = (
        "scan_id",
        "device_uid",
        "device_type",
        "scan_status",
        "is_registered",
    )

    list_filter = (
        "scan_status",
        "is_registered",
        "device_type",
        "device_category",
    )

    search_fields = ("scan_id", "device_uid", "device_name")
    readonly_fields = ("scan_id",)

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        """
        NetworkScanResultModel is not managed via CRUD.
        Redirect to Discover panel instead.
        """
        return redirect(reverse("admin:commands_discover"))



from apps.commands.infrastructure.models import (
    CommandModel,
    CommandAttemptModel,
    NetworkScanResultModel,
    CommandAliasModel,
)


@admin.register(CommandAliasModel)
class CommandAliasAdmin(admin.ModelAdmin):
    list_display = (
        "device_category",
        "device_type",
        "command_category",
        "command_type",
        "resolved_command_name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "device_category",
        "device_type",
        "command_category",
        "is_active",
    )

    search_fields = (
        "device_category",
        "device_type",
        "command_category",
        "command_type",
        "resolved_command_name",
    )

    ordering = ("device_category", "device_type", "command_category")
