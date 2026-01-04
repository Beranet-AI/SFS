from django import forms

from apps.commands.domain.enums.command_status import CommandStatus


class ReceiveResultForm(forms.Form):
    command_id = forms.UUIDField()
    attempt_no = forms.IntegerField(min_value=1)
    status = forms.ChoiceField(
        choices=[
            (CommandStatus.SUCCEEDED.value, "succeeded"),
            (CommandStatus.FAILED.value, "failed"),
            (CommandStatus.TIMED_OUT.value, "timed_out"),
            (CommandStatus.CANCELLED.value, "cancelled"),
        ]
    )
    result = forms.JSONField(required=False)
    error_code = forms.CharField(max_length=64, required=False)
    error_message = forms.CharField(required=False)
    meta = forms.JSONField(required=False)
