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

    def __str__(self):
        return f"{self.title} ({self.course})"


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
