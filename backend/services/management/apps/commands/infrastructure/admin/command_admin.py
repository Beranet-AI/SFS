from django import forms
from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.urls import path

from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.domain.enums.command_target_kind import CommandTargetKind
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.exceptions.command_exceptions import CommandValidationError
from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)
from apps.commands.infrastructure.models.command_attempt_model import CommandAttemptModel
from apps.commands.infrastructure.models.command_model import CommandModel


class SendCommandForm(forms.Form):
    command_type = forms.ChoiceField(
        choices=[(c.value, c.value) for c in CommandType]
    )
    target_kind = forms.ChoiceField(
        choices=[(k.value, k.value) for k in CommandTargetKind]
    )
    target_id = forms.CharField(max_length=64)
    edge_node_id = forms.CharField(max_length=64, required=False)
    payload = forms.JSONField(required=False)
    idempotency_key = forms.CharField(max_length=128, required=False)
    ack_deadline_sec = forms.IntegerField(required=False, min_value=1)
    result_deadline_sec = forms.IntegerField(required=False, min_value=1)
    max_attempts = forms.IntegerField(required=False, min_value=1)
    backoff_sec = forms.IntegerField(required=False, min_value=0)


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

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(
                "send/",
                self.admin_site.admin_view(self.send_command_view),
                name="commands_commandmodel_send",
            )
        ] + urls

    def send_command_view(self, request):
        context = {
            **self.admin_site.each_context(request),
            "title": "Send Command",
        }

        command = None

        if request.method == "POST":
            form = SendCommandForm(request.POST)
            if form.is_valid():
                dto = SendCommandInputDTO(
                    command_name=form.cleaned_data["command_type"],
                    target_kind=form.cleaned_data["target_kind"],
                    target_id=form.cleaned_data["target_id"],
                    edge_node_id=form.cleaned_data["edge_node_id"] or None,
                    payload=form.cleaned_data.get("payload"),
                    idempotency_key=form.cleaned_data.get("idempotency_key"),
                    ack_deadline_sec=form.cleaned_data.get("ack_deadline_sec"),
                    result_deadline_sec=form.cleaned_data.get("result_deadline_sec"),
                    max_attempts=form.cleaned_data.get("max_attempts"),
                    backoff_sec=form.cleaned_data.get("backoff_sec"),
                )

                try:
                    use_case = SendCommandUseCase(
                        repository=DjangoCommandRepository(),
                        edge_client=EdgeControllerClient(),
                    )
                    command = use_case.execute(
                        dto,
                        created_by=request.user.get_username()
                        or str(request.user),
                    )
                    messages.success(request, "Command dispatched successfully.")
                    form = SendCommandForm()
                except CommandValidationError as exc:
                    form.add_error(None, str(exc))
        else:
            form = SendCommandForm()

        context["form"] = form
        context["command"] = command
        return TemplateResponse(
            request,
            "admin/commands/send_command.html",
            context,
        )


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
