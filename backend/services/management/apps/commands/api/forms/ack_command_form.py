from django import forms


class AckCommandForm(forms.Form):
    command_id = forms.UUIDField()
    attempt_no = forms.IntegerField(min_value=1)
    executor_receipt = forms.CharField(max_length=128, required=False)
    meta = forms.JSONField(required=False)
