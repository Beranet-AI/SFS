from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse

from apps.commands.api.admin_views.dependencies import (
    build_start_network_scan_use_case,
)
from apps.commands.api.forms.network_scan_form import NetworkScanForm
from apps.commands.application.use_cases.start_network_scan.input_dto import (
    StartNetworkScanInputDTO,
)
from apps.commands.domain.exceptions.invalid_target import InvalidTargetError


@staff_member_required
def discover_view(request):
    context = {
        **admin.site.each_context(request),
        "title": "Discover Network",
    }
    scan_id = None
    command_id = None

    if request.method == "POST":
        action = request.POST.get("action", "discover")
        form = NetworkScanForm(request.POST)
        if action != "discover":
            messages.error(request, "Unsupported action.")
        elif form.is_valid():
            use_case = build_start_network_scan_use_case()
            try:
                output = use_case.execute(
                    StartNetworkScanInputDTO(
                        edge_node_id=form.cleaned_data["edge_node_id"]
                    ),
                    created_by=request.user.get_username()
                    or str(request.user),
                )
                scan_id = output.scan_id
                command_id = output.command_id
                messages.success(
                    request,
                    "Network scan started successfully.",
                )
            except InvalidTargetError as exc:
                form.add_error(None, str(exc))
            except Exception as exc:
                messages.error(request, f"Discovery failed: {exc}")
    else:
        form = NetworkScanForm()

    context["form"] = form
    context["scan_id"] = scan_id
    context["command_id"] = command_id
    context["results"] = []
    return TemplateResponse(
        request,
        "admin/commands/discover.html",
        context,
    )
