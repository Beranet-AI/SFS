from django import forms


class DeleteUserForm(forms.Form):
    user_id = forms.CharField()
