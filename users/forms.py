from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from categories.models import University

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    university = forms.ModelChoiceField(queryset=University.objects.none())


    class Meta:
        model = User
        fields = ("username","email","password1","password2","university")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from categories.models import University
        self.fields['university'].queryset = University.objects.all()
