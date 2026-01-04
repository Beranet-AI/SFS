from django import forms


class UpdateUserForm(forms.Form):
    user_id = forms.CharField()
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    is_active = forms.BooleanField(required=False)
    is_active_account = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
