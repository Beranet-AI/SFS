from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse

from apps.commands.application.services.command_dispatcher import CommandDispatcher
from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.exceptions.invalid_target import InvalidTargetError
from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)
from apps.commands.infrastructure.executors.device_command_executor import (
    DeviceCommandExecutor,
)
from apps.commands.infrastructure.executors.edge_command_executor import (
    EdgeCommandExecutor,
)
from apps.commands.infrastructure.repositories.django_capability_repository import (
    DjangoCapabilityRepository,
)
from apps.commands.infrastructure.repositories.django_command_repository import (
    DjangoCommandRepository,
)
from apps.devices.application.services.device_service import DeviceService
from apps.devices.models import DeviceStatus
from apps.devices.models import DeviceModel


@admin.register(DeviceModel)
class DeviceAdmin(admin.ModelAdmin):
    change_form_template = "admin/devices/devicemodel/change_form.html"

    list_display = (
        "id",
        "kind",
        "display_name",
        "status",
        "farm_id",
        "livestock_id",
        "updated_at",
    )

    list_filter = (
        "kind",
        "status",
        "farm_id",
    )

    search_fields = (
        "display_name",
        "id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<int:device_id>/turn-on/",
                self.admin_site.admin_view(self.turn_on_view),
                name="devices_devicemodel_turn_on",
            ),
            path(
                "<int:device_id>/turn-off/",
                self.admin_site.admin_view(self.turn_off_view),
                name="devices_devicemodel_turn_off",
            ),
        ]
        return custom + urls

    def turn_on_view(self, request, device_id: int):
        if request.method != "POST":
            return redirect(
                reverse("admin:devices_devicemodel_change", args=[device_id])
            )

        try:
            device_service = DeviceService()
            device = device_service.get_by_id(device_id=str(device_id))
            if device.status == DeviceStatus.DISABLED:
                raise InvalidTargetError(
                    "Device is disabled and cannot be turned on."
                )

            edge_node_id = (device.metadata or {}).get("edge_node_id") or (
                device.metadata or {}
            ).get("edge_id")
            capability_repository = DjangoCapabilityRepository()
            edge_client = EdgeControllerClient()
            dispatcher = CommandDispatcher(
                edge_executor=EdgeCommandExecutor(edge_client=edge_client),
                device_executor=DeviceCommandExecutor(edge_client=edge_client),
                capability_repository=capability_repository,
            )
            SendCommandUseCase(
                repository=DjangoCommandRepository(),
                dispatcher=dispatcher,
                capability_repository=capability_repository,
            ).execute(
                SendCommandInputDTO(
                    command_name=CommandType.ON_OFF.value,
                    command_type=CommandType.ON_OFF.value,
                    target_kind="device",
                    target_id=device.serial,
                    edge_node_id=edge_node_id,
                    payload={"device_id": device.serial, "action": "ON"},
                ),
                created_by=request.user.get_username() or str(request.user),
            )
            messages.success(request, "Power on command sent.")
        except InvalidTargetError as exc:
            messages.error(request, str(exc))

        return redirect(
            reverse("admin:devices_devicemodel_change", args=[device_id])
        )

    def turn_off_view(self, request, device_id: int):
        if request.method != "POST":
            return redirect(
                reverse("admin:devices_devicemodel_change", args=[device_id])
            )

        try:
            device_service = DeviceService()
            device = device_service.get_by_id(device_id=str(device_id))
            if device.status == DeviceStatus.DISABLED:
                raise InvalidTargetError(
                    "Device is disabled and cannot be turned off."
                )

            edge_node_id = (device.metadata or {}).get("edge_node_id") or (
                device.metadata or {}
            ).get("edge_id")
            capability_repository = DjangoCapabilityRepository()
            edge_client = EdgeControllerClient()
            dispatcher = CommandDispatcher(
                edge_executor=EdgeCommandExecutor(edge_client=edge_client),
                device_executor=DeviceCommandExecutor(edge_client=edge_client),
                capability_repository=capability_repository,
            )
            SendCommandUseCase(
                repository=DjangoCommandRepository(),
                dispatcher=dispatcher,
                capability_repository=capability_repository,
            ).execute(
                SendCommandInputDTO(
                    command_name=CommandType.ON_OFF.value,
                    command_type=CommandType.ON_OFF.value,
                    target_kind="device",
                    target_id=device.serial,
                    edge_node_id=edge_node_id,
                    payload={"device_id": device.serial, "action": "OFF"},
                ),
                created_by=request.user.get_username() or str(request.user),
            )
            messages.success(request, "Power off command sent.")
        except InvalidTargetError as exc:
            messages.error(request, str(exc))

        return redirect(
            reverse("admin:devices_devicemodel_change", args=[device_id])
        )
