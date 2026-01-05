from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse

from apps.commands.infrastructure.repositories.django_command_repository import (
    DjangoCommandRepository,
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
            command = DjangoCommandRepository().get(
                command_id=str(form.cleaned_data["command_id"])
            )
    else:
        form = GetCommandForm()

    context["form"] = form
    context["command"] = command
    return TemplateResponse(
        request,
        "admin/commands/command_dashboard.html",
        context,
    )
