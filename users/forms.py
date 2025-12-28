from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # özel kullanıcı modelin

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-posta", required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
