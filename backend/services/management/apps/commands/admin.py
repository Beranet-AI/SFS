# backend/services/management/apps/commands/admin.py
from django.contrib import admin
from .models import CommandModel, CommandAttemptModel


@admin.register(CommandModel)
class CommandAdmin(admin.ModelAdmin):
    list_display = ("id", "command_name", "target_kind", "target_id", "edge_node_id", "status", "created_at")
    list_filter = ("status", "target_kind", "command_name")
    search_fields = ("id", "target_id", "edge_node_id", "idempotency_key")
    readonly_fields = ("created_at", "acked_at", "started_at", "finished_at")

    fieldsets = (
        ("Identity", {"fields": ("id", "command_name", "idempotency_key")}),
        ("Target", {"fields": ("target_kind", "target_id", "edge_node_id")}),
        ("Payload", {"fields": ("payload",)}),
        ("Policy", {"fields": ("ack_deadline_sec", "result_deadline_sec", "max_attempts")}),
        ("Status", {"fields": ("status", "created_by", "created_at", "acked_at", "started_at", "finished_at")}),
        ("Latest Result / Error", {"fields": ("last_result", "last_error_code", "last_error_message")}),
    )


@admin.register(CommandAttemptModel)
class CommandAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "command", "attempt_no", "status", "created_at", "dispatched_at", "acked_at", "result_at")
    list_filter = ("status",)
    search_fields = ("id", "command__id", "executor_receipt")
    readonly_fields = ("created_at",)
