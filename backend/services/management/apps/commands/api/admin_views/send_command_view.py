from django.contrib import admin, messages
from django.template.response import TemplateResponse

from apps.commands.api.forms.send_command_form import SendCommandForm
from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.domain.exceptions.command_execution_error import (
    CommandExecutionError,
)
from apps.commands.domain.exceptions.invalid_target import InvalidTargetError
from apps.commands.domain.exceptions.unsupported_command import (
    UnsupportedCommandError,
)
from apps.commands.api.admin_views.dependencies import (
    build_send_command_use_case,
)


def send_command_view(request):
    context = {
        **admin.site.each_context(request),
        "title": "Send Command",
    }

    command = None

    if request.method == "POST":
        form = SendCommandForm(request.POST)
        if form.is_valid():
            dto = SendCommandInputDTO(
                command_name=form.cleaned_data["command_type"],
                command_type=form.cleaned_data["command_type"],
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
            use_case = build_send_command_use_case()
            try:
                command = use_case.execute(
                    dto,
                    created_by=request.user.get_username() or str(request.user),
                )
                messages.success(request, "Command dispatched successfully.")
                form = SendCommandForm()
            except (
                CommandExecutionError,
                InvalidTargetError,
                UnsupportedCommandError,
            ) as exc:
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
