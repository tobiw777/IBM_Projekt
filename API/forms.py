from django import forms
from django.contrib.auth.models import User
from .models import models, Code


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Code
        labels = {
            'token': 'Kod uwierzytelniający',
        }
        fields = ('token',)
