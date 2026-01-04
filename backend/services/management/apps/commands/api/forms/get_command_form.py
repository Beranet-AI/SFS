from django import forms


class GetCommandForm(forms.Form):
    command_id = forms.UUIDField()
