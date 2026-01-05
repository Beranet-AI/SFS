from django import forms
from django.contrib import admin, messages
from django.template.response import TemplateResponse

from apps.commands.application.services.discovery_result_service import (
    DiscoveryResultService,
)
from apps.commands.application.use_cases.get_command.input_dto import (
    GetCommandInputDTO,
)
from apps.commands.application.use_cases.get_command.use_case import (
    GetCommandUseCase,
)
from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)
from apps.commands.application.use_cases.receive_result.use_case import (
    ReceiveResultUseCase,
)
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
from apps.commands.infrastructure.repositories.command_attempt_repository import (
    DjangoCommandAttemptRepository,
)
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)
from apps.commands.infrastructure.repositories.discovered_device_repository import (
    DjangoDiscoveredDeviceRepository,
)
from apps.commands.infrastructure.repositories.discovery_session_repository import (
    DjangoDiscoverySessionRepository,
)


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


class ReceiveResultForm(forms.Form):
    command_id = forms.UUIDField()
    attempt_no = forms.IntegerField(min_value=1)
    status = forms.CharField(max_length=32)
    result = forms.JSONField(required=False)
    error_code = forms.CharField(required=False)
    error_message = forms.CharField(required=False, widget=forms.Textarea)
    meta = forms.JSONField(required=False)


class GetCommandForm(forms.Form):
    command_id = forms.UUIDField()


def load_command_detail(request, queryset):
    command = queryset.first()
    if not command:
        return None
    use_case = GetCommandUseCase(DjangoCommandRepository())
    return use_case.execute(GetCommandInputDTO(command_id=str(command.id)))


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


def receive_result_view(request):
    context = {
        **admin.site.each_context(request),
        "title": "Receive Result",
    }

    received = None

    if request.method == "POST":
        form = ReceiveResultForm(request.POST)
        if form.is_valid():
            dto = ReceiveResultInputDTO(
                command_id=str(form.cleaned_data["command_id"]),
                attempt_no=form.cleaned_data["attempt_no"],
                status=form.cleaned_data["status"],
                result=form.cleaned_data.get("result") or {},
                error_code=form.cleaned_data.get("error_code") or "",
                error_message=form.cleaned_data.get("error_message") or "",
                meta=form.cleaned_data.get("meta") or {},
            )
            use_case = ReceiveResultUseCase(
                command_repository=DjangoCommandRepository(),
                attempt_repository=DjangoCommandAttemptRepository(),
                discovery_result_service=DiscoveryResultService(
                    session_repository=DjangoDiscoverySessionRepository(),
                    device_repository=DjangoDiscoveredDeviceRepository(),
                ),
            )
            use_case.execute(dto)
            received = dto
            messages.success(request, "Result recorded successfully.")
            form = ReceiveResultForm()
    else:
        form = ReceiveResultForm()

    context["form"] = form
    context["received"] = received
    return TemplateResponse(
        request,
        "admin/commands/receive_result.html",
        context,
    )


def command_dashboard_view(request):
    context = {
        **admin.site.each_context(request),
        "title": "Command Dashboard",
    }

    command = None

    if request.method == "POST":
        form = GetCommandForm(request.POST)
        if form.is_valid():
            dto = GetCommandInputDTO(
                command_id=str(form.cleaned_data["command_id"])
            )
            command = GetCommandUseCase(DjangoCommandRepository()).execute(dto)
    else:
        form = GetCommandForm()

    context["form"] = form
    context["command"] = command
    return TemplateResponse(
        request,
        "admin/commands/command_dashboard.html",
        context,
    )
