from django import forms
from .models import Note
from django.core.exceptions import ValidationError
from uniedunote.file_security import get_file_validation_error


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['university', 'faculty', 'department', 'semester', 'course', 'title', 'description', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            error_message = get_file_validation_error(file)
            if error_message:
                raise ValidationError(error_message)
        return file