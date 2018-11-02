from django import forms

from .validators import validate_username, validate_password


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=150, validators=[validate_username])
    password = forms.CharField(max_length=128, strip=False, validators=[validate_password])

    def get_username(self):
        return self.cleaned_data['username']

    def get_password(self):
        return self.cleaned_data['password']
