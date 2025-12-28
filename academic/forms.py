from django import forms
from django.contrib.auth.models import User
from .models import Note, Profile

# --- NOT YÜKLEME FORMU ---
class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Örn: 2024 Fizik 1 Final Soruları'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Not içeriği hakkında kısa bilgi...'}),
        }

# --- PROFİL GÜNCELLEME FORMLARI ---
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['university', 'bio', 'avatar']