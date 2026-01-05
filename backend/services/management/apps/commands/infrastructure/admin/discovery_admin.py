from django import forms
from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from apps.commands.application.use_cases.register_discovered_device.input_dto import (
    RegisterDiscoveredDeviceInputDTO,
)
from apps.commands.application.use_cases.register_discovered_device.use_case import (
    RegisterDiscoveredDeviceUseCase,
)
from apps.commands.application.use_cases.start_discovery.input_dto import (
    StartDiscoveryInputDTO,
)
from apps.commands.application.use_cases.start_discovery.use_case import (
    StartDiscoveryUseCase,
)
from apps.commands.domain.exceptions.command_exceptions import CommandValidationError
from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)
from apps.commands.infrastructure.models.devices import DiscoveredDeviceModel
from apps.commands.infrastructure.models.discovery_session_model import (
    DiscoverySessionModel,
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


class StartDiscoveryForm(forms.Form):
    edge_node_id = forms.CharField(max_length=64, label="Edge node")


@admin.register(DiscoverySessionModel)
class DiscoverySessionAdmin(admin.ModelAdmin):
    change_list_template = "admin/commands/discovery_session/change_list.html"
    change_form_template = "admin/commands/discovery_session/change_form.html"

    list_display = (
        "id",
        "edge_node_id",
        "status",
        "started_at",
        "finished_at",
        "device_count",
    )
    list_filter = ("status", "edge_node_id")
    search_fields = ("id", "edge_node_id", "command_id")
    readonly_fields = (
        "id",
        "edge_node_id",
        "command",
        "status",
        "started_by",
        "started_at",
        "finished_at",
        "device_count",
        "error_message",
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "start/",
                self.admin_site.admin_view(self.start_discovery_view),
                name="commands_discovery_start",
            ),
            path(
                "<uuid:session_id>/register-device/<uuid:device_id>/",
                self.admin_site.admin_view(self.register_device_view),
                name="commands_discovery_register_device",
            ),
        ]
        return custom + urls

    def changelist_view(
        self, request: HttpRequest, extra_context: dict | None = None
    ) -> HttpResponse:
        context = extra_context or {}
        context["form"] = StartDiscoveryForm()
        return super().changelist_view(request, extra_context=context)

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: str | None = None,
        form_url: str = "",
        extra_context: dict | None = None,
    ) -> HttpResponse:
        context = extra_context or {}
        if object_id:
            context["devices"] = DiscoveredDeviceModel.objects.filter(
                session_id=object_id
            ).order_by("device_id")
        return super().changeform_view(
            request,
            object_id=object_id,
            form_url=form_url,
            extra_context=context,
        )

    def start_discovery_view(self, request: HttpRequest) -> HttpResponse:
        context = {
            **self.admin_site.each_context(request),
            "title": "Discover Devices",
        }

        if request.method == "POST":
            form = StartDiscoveryForm(request.POST)
            if form.is_valid():
                use_case = StartDiscoveryUseCase(
                    session_repository=DjangoDiscoverySessionRepository(),
                    command_repository=DjangoCommandRepository(),
                    edge_client=EdgeControllerClient(),
                )
                try:
                    session = use_case.execute(
                        StartDiscoveryInputDTO(
                            edge_node_id=form.cleaned_data["edge_node_id"]
                        ),
                        created_by=request.user.get_username()
                        or str(request.user),
                    )
                    messages.success(request, "Discovery started.")
                    return redirect(
                        reverse(
                            "admin:commands_discoverysessionmodel_change",
                            args=[session.id],
                        )
                    )
                except CommandValidationError as exc:
                    form.add_error(None, str(exc))
        else:
            form = StartDiscoveryForm()

        context["form"] = form
        return TemplateResponse(
            request,
            "admin/commands/discovery_session/start_discovery.html",
            context,
        )

    def register_device_view(
        self, request: HttpRequest, session_id: str, device_id: str
    ) -> HttpResponse:
        if request.method != "POST":
            return redirect(
                reverse(
                    "admin:commands_discoverysessionmodel_change",
                    args=[session_id],
                )
            )

        use_case = RegisterDiscoveredDeviceUseCase(
            discovered_device_repository=DjangoDiscoveredDeviceRepository(),
        )
        use_case.execute(
            RegisterDiscoveredDeviceInputDTO(
                discovered_device_id=str(device_id)
            )
        )
        messages.success(request, "Device registered.")
        return redirect(
            reverse(
                "admin:commands_discoverysessionmodel_change",
                args=[session_id],
            )
        )
