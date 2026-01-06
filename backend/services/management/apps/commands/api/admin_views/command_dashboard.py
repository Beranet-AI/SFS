from django import forms
from django.contrib import admin, messages
from django.template.response import TemplateResponse

from apps.commands.api.admin_views.dependencies import (
    build_get_command_use_case,
)
from apps.commands.application.use_cases.get_command.input_dto import (
    GetCommandInputDTO,
)


class GetCommandForm(forms.Form):
    command_id = forms.UUIDField()


def command_dashboard_view(request):
    context = {
        **admin.site.each_context(request),
        "title": "Command Dashboard",
    }

    command = None

    if request.method == "POST":
        form = GetCommandForm(request.POST)
        if form.is_valid():
            use_case = build_get_command_use_case()
            try:
                output = use_case.execute(
                    GetCommandInputDTO(
                        command_id=str(form.cleaned_data["command_id"])
                    )
                )
                command = output.command
            except Exception as exc:
                messages.error(request, f"Failed to load command: {exc}")
    else:
        form = GetCommandForm()

    context["form"] = form
    context["command"] = command
    return TemplateResponse(
        request,
        "admin/commands/command_dashboard.html",
        context,
    )
