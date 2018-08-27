from django import forms
from django.contrib.auth.models import User
from .models import models, Code, Glos


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Code
        labels = {
            'token': 'Kod uwierzytelniający',
        }
        fields = ('token',)

class GlosForm(forms.ModelForm):
    class Meta:
        model = Glos
        labels = {
            'wynik': 'Odpowiedź',
        }
        fields = ['wynik']