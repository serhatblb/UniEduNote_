from django.db import models
from users.models import User
from categories.models import University, Faculty, Department, Course

class Note(models.Model):
    SEMESTER_CHOICES = [
        ('BAHAR-2024', 'Bahar 2024'),
        ('GÜZ-2024', 'Güz 2024'),
        ('BAHAR-2025', 'Bahar 2025'),
        ('GÜZ-2025', 'Güz 2025'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['-uploaded_at']),
            models.Index(fields=['-likes']),
            models.Index(fields=['-download_count']),
            models.Index(fields=['university', '-uploaded_at']),
            models.Index(fields=['department', '-uploaded_at']),
            models.Index(fields=['course', '-uploaded_at']),
        ]

    def __str__(self):
        return f"{self.title} ({self.course})"
    
    def get_file_icon(self):
        """Dosya tipine göre ikon döndürür"""
        if not self.file:
            return "fa-file"
        
        file_name = self.file.name.lower()
        
        # PDF
        if file_name.endswith('.pdf'):
            return "fa-file-pdf"
        # Word
        elif file_name.endswith(('.doc', '.docx')):
            return "fa-file-word"
        # Excel
        elif file_name.endswith(('.xls', '.xlsx')):
            return "fa-file-excel"
        # PowerPoint
        elif file_name.endswith(('.ppt', '.pptx')):
            return "fa-file-powerpoint"
        # Resimler
        elif file_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
            return "fa-file-image"
        # Zip/Rar
        elif file_name.endswith(('.zip', '.rar', '.7z')):
            return "fa-file-zipper"
        # Text
        elif file_name.endswith('.txt'):
            return "fa-file-lines"
        # Default
        else:
            return "fa-file"


# 💬 Yorum Modeli
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.note.title}"


# ❤️ Beğeni Modeli
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='likes_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'note')  # aynı kullanıcı aynı notu iki kez beğenemez

    def __str__(self):
        return f"{self.user.username} → {self.note.title}"


# 🔖 Bookmark (Kaydedilenler)
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'note')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} ★ {self.note.title}"


# 🚩 İçerik Raporlama
class Report(models.Model):
    REASONS = [
        ('spam', 'Spam / Gereksiz İçerik'),
        ('yanlis_bilgi', 'Yanlış / Yanıltıcı Bilgi'),
        ('uygunsuz', 'Uygunsuz İçerik'),
        ('telif_hakki', 'Telif Hakkı İhlali'),
        ('kopya', 'Kopya / Mükerrer Not'),
        ('diger', 'Diğer'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='reports')
    reason = models.CharField(max_length=30, choices=REASONS)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('reporter', 'note')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reporter.username} → {self.note.title} ({self.reason})"
