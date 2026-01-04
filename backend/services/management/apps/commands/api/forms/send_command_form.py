from django import forms

from apps.commands.domain.enums.command_target_kind import CommandTargetKind


class SendCommandForm(forms.Form):
    command_name = forms.CharField(max_length=120)
    target_kind = forms.ChoiceField(
        choices=[(kind.value, kind.value) for kind in CommandTargetKind]
    )
    target_id = forms.CharField(max_length=64)
    edge_node_id = forms.CharField(max_length=64, required=False)
    payload = forms.JSONField(required=False)
    idempotency_key = forms.CharField(max_length=128, required=False)
    ack_deadline_sec = forms.IntegerField(required=False, min_value=1)
    result_deadline_sec = forms.IntegerField(required=False, min_value=1)
    max_attempts = forms.IntegerField(required=False, min_value=1)
    backoff_sec = forms.IntegerField(required=False, min_value=0)
