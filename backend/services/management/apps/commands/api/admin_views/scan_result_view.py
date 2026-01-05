from django import forms
from django.contrib import admin, messages
from django.template.response import TemplateResponse

from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)
from apps.commands.application.use_cases.receive_result.use_case import (
    ReceiveResultUseCase,
)
from apps.commands.infrastructure.repositories.django_command_repository import (
    DjangoCommandRepository,
)


class ReceiveResultForm(forms.Form):
    command_id = forms.UUIDField()
    attempt_no = forms.IntegerField(min_value=1)
    status = forms.CharField(max_length=32)
    result = forms.JSONField(required=False)
    error_code = forms.CharField(required=False)
    error_message = forms.CharField(required=False, widget=forms.Textarea)
    meta = forms.JSONField(required=False)


def scan_result_view(request):
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
