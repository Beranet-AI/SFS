from django import forms


class CreateUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    phone_number = forms.CharField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
