# notes/forms.py
from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'university',
            'faculty',
            'department',
            'course',
            'semester',
            'title',
            'description',
            'file',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
