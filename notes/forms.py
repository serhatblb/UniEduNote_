from django import forms
from .models import Note
from django.core.exceptions import ValidationError


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['university', 'faculty', 'department', 'semester', 'course', 'title', 'description', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # İzin verilen uzantılar
            allowed_extensions = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar']
            ext = file.name.split('.')[-1].lower()

            if ext not in allowed_extensions:
                raise ValidationError("Sadece belge ve görsel yükleyebilirsiniz. Video yüklenemez.")

            # Boyut kontrolü (Örn: 20MB)
            if file.size > 20 * 1024 * 1024:
                raise ValidationError("Dosya boyutu 20MB'dan büyük olamaz.")

        return file