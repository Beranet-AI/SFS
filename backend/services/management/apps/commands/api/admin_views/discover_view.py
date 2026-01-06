# apps/commands/api/admin_views/discover_view.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.commands.application.use_cases.discover_network.use_case import (
    DiscoverNetworkUseCase,
)
from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)


@staff_member_required
def discover_view(request):
    if request.method == "POST":
        try:
            edge_client = EdgeControllerClient()
            use_case = DiscoverNetworkUseCase(edge_client=edge_client)

            result = use_case.execute(
                triggered_by=request.user.get_username()
            )

            messages.success(
                request,
                f"Network discovery started. Devices found: {len(result.devices)}",
            )
            return redirect("admin:commands_networkscanresult_changelist")

        except Exception as exc:
            messages.error(request, f"Discovery failed: {exc}")

    return render(
        request,
        "admin/commands/send_command.html",
        {
            "title": "Discover Network",
            "action": "discover",
        },
    )
