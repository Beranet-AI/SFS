from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse

from apps.commands.application.use_cases.turn_device_off.input_dto import (
    TurnDeviceOffInputDTO,
)
from apps.commands.application.use_cases.turn_device_off.use_case import (
    TurnDeviceOffUseCase,
)
from apps.commands.application.use_cases.turn_device_on.input_dto import (
    TurnDeviceOnInputDTO,
)
from apps.commands.application.use_cases.turn_device_on.use_case import (
    TurnDeviceOnUseCase,
)
from apps.commands.domain.exceptions.command_exceptions import CommandValidationError
from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)
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
            TurnDeviceOnUseCase(
                command_repository=DjangoCommandRepository(),
                edge_client=EdgeControllerClient(),
            ).execute(
                TurnDeviceOnInputDTO(device_id=str(device_id)),
                created_by=request.user.get_username() or str(request.user),
            )
            messages.success(request, "Power on command sent.")
        except CommandValidationError as exc:
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
            TurnDeviceOffUseCase(
                command_repository=DjangoCommandRepository(),
                edge_client=EdgeControllerClient(),
            ).execute(
                TurnDeviceOffInputDTO(device_id=str(device_id)),
                created_by=request.user.get_username() or str(request.user),
            )
            messages.success(request, "Power off command sent.")
        except CommandValidationError as exc:
            messages.error(request, str(exc))

        return redirect(
            reverse("admin:devices_devicemodel_change", args=[device_id])
        )
