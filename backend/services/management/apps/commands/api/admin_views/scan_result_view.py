from django import forms
from django.contrib import admin, messages
from django.template.response import TemplateResponse

from apps.commands.api.admin_views.dependencies import (
    build_receive_result_use_case,
)
from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)


class ReceiveResultForm(forms.Form):
    command_id = forms.UUIDField()
    attempt_no = forms.IntegerField(min_value=1)
    status = forms.CharField(max_length=32)
    payload = forms.JSONField(required=False)
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
                payload=form.cleaned_data.get("payload") or {},
                error_code=form.cleaned_data.get("error_code") or "",
                error_message=form.cleaned_data.get("error_message") or "",
                meta=form.cleaned_data.get("meta") or {},
            )
            use_case = build_receive_result_use_case()
            try:
                use_case.execute(dto)
                received = dto
                messages.success(request, "Result recorded successfully.")
                form = ReceiveResultForm()
            except Exception as exc:
                messages.error(request, f"Failed to record result: {exc}")
    else:
        form = ReceiveResultForm()

    context["form"] = form
    context["received"] = received
    return TemplateResponse(
        request,
        "admin/commands/receive_result.html",
        context,
    )
