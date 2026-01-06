from django import forms
from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from apps.commands.application.services.command_dispatcher import CommandDispatcher
from apps.commands.application.use_cases.start_network_scan.input_dto import (
    StartNetworkScanInputDTO,
)
from apps.commands.application.use_cases.start_network_scan.use_case import (
    StartNetworkScanUseCase,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)
from apps.commands.infrastructure.executors.device_command_executor import (
    DeviceCommandExecutor,
)
from apps.commands.infrastructure.executors.edge_command_executor import (
    EdgeCommandExecutor,
)
from apps.commands.infrastructure.models.network_scan_result_model import (
    NetworkScanResultModel,
)
from apps.commands.infrastructure.repositories.django_capability_repository import (
    DjangoCapabilityRepository,
)
from apps.commands.infrastructure.repositories.django_command_repository import (
    DjangoCommandRepository,
)
from apps.devices.application.use_cases.register_control_device.input_dto import (
    RegisterControlDeviceInputDTO,
)
from apps.devices.application.use_cases.register_control_device.use_case import (
    RegisterControlDeviceUseCase,
)
from apps.telemetry.application.use_cases.register_schema.input_dto import (
    RegisterSchemaInputDTO,
)
from apps.telemetry.application.use_cases.register_schema.use_case import (
    RegisterTelemetrySchemaUseCase,
)


class DiscoverForm(forms.Form):
    edge_node_id = forms.CharField(label="Edge Node ID", max_length=64)


def _register_device(*, result: NetworkScanResultModel, created_by: str) -> None:
    capabilities = {
        "supported_command_categories": result.supported_command_categories,
        "adapter_type": result.adapter_type,
        "protocol": result.protocol,
        "direction": result.direction,
        "supports_commands": result.supports_commands,
    }
    metadata = {
        "device_category": result.device_category,
        "device_type": result.device_type,
        "ip_address": result.ip_address,
        "port": result.port,
        "network_address": result.network_address,
        "signal_strength": result.signal_strength,
        "firmware_version": result.firmware_version,
        "vendor": result.vendor,
        "model": result.model,
        "battery_level": result.battery_level,
        "last_seen_at": result.last_seen_at.isoformat() if result.last_seen_at else None,
        "discovered_at": result.discovered_at.isoformat()
        if result.discovered_at
        else None,
        "scan_status": result.scan_status,
        "raw_capabilities": result.raw_capabilities,
    }
    RegisterControlDeviceUseCase().execute(
        RegisterControlDeviceInputDTO(
            serial=result.device_uid,
            display_name=result.device_name or result.device_uid,
            metadata=metadata,
            capabilities=capabilities,
            kind=result.device_category or "device",
            farm_id="",
            barn_id="",
            zone_id="",
            created_by=created_by,
        )
    )

    raw_capabilities = result.raw_capabilities or {}
    if not isinstance(raw_capabilities, dict):
        raw_capabilities = {}

    RegisterTelemetrySchemaUseCase().execute(
        RegisterSchemaInputDTO(
            device_type=result.device_type or result.device_category or "device",
            json_schema=raw_capabilities.get("json_schema") or {},
            raw_example=raw_capabilities.get("raw_example") or {},
            created_by=created_by,
        )
    )


def discover_view(request):
    context = {
        **admin.site.each_context(request),
        "title": "Discover",
    }
    scan_id = request.GET.get("scan_id") or request.POST.get("scan_id")
    results = NetworkScanResultModel.objects.none()
    if scan_id:
        results = NetworkScanResultModel.objects.filter(scan_id=scan_id).order_by(
            "device_uid"
        )
    else:
        latest = NetworkScanResultModel.objects.order_by("-discovered_at").first()
        if latest:
            scan_id = str(latest.scan_id)
            results = NetworkScanResultModel.objects.filter(scan_id=scan_id).order_by(
                "device_uid"
            )

    discover_form = DiscoverForm()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "discover":
            discover_form = DiscoverForm(request.POST)
            if discover_form.is_valid():
                edge_node_id = discover_form.cleaned_data["edge_node_id"]
                capability_repository = DjangoCapabilityRepository()
                edge_client = EdgeControllerClient()
                dispatcher = CommandDispatcher(
                    edge_executor=EdgeCommandExecutor(edge_client=edge_client),
                    device_executor=DeviceCommandExecutor(edge_client=edge_client),
                    capability_repository=capability_repository,
                )
                use_case = StartNetworkScanUseCase(
                    send_command_use_case=SendCommandUseCase(
                        repository=DjangoCommandRepository(),
                        dispatcher=dispatcher,
                        capability_repository=capability_repository,
                    )
                )
                output = use_case.execute(
                    StartNetworkScanInputDTO(edge_node_id=edge_node_id),
                    created_by=request.user.get_username() or str(request.user),
                )
                messages.success(request, "Network scan started.")
                return redirect(
                    f"{reverse('admin:commands_discover')}?scan_id={output.scan_id}"
                )
        elif action == "register":
            selected_ids = request.POST.getlist("selected_devices")
            if not selected_ids:
                messages.error(request, "No devices selected for registration.")
            else:
                created_by = request.user.get_username() or str(request.user)
                with transaction.atomic():
                    for result in NetworkScanResultModel.objects.filter(
                        id__in=selected_ids, is_registered=False
                    ):
                        _register_device(result=result, created_by=created_by)
                        result.is_registered = True
                        result.save(update_fields=["is_registered", "updated_at"])
                messages.success(request, "Selected devices registered.")
                if scan_id:
                    return redirect(
                        f"{reverse('admin:commands_discover')}?scan_id={scan_id}"
                    )
                return redirect(reverse("admin:commands_discover"))

    context["discover_form"] = discover_form
    context["scan_id"] = scan_id
    context["results"] = results
    return TemplateResponse(
        request,
        "admin/commands/discover.html",
        context,
    )
