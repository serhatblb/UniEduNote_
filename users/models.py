from django.contrib.auth.models import AbstractUser
from django.db import models
from categories.models import University


class User(AbstractUser):
    # Profil Alanları
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="students")
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)
    email = models.EmailField(unique=True)

    # Yeni: Premium Üyelik
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def rank(self):
        """Oyunlaştırma: Puanına göre rütbe getirir"""
        # Not yükleme 10 puan, İndirilme 1 puan
        uploads = self.note_set.count()
        downloads = sum(n.download_count for n in self.note_set.all())
        score = (uploads * 10) + downloads

        if score < 10: return "🌱 Çaylak"
        if score < 50: return "✏️ Öğrenci"
        if score < 100: return "🎓 Mezun"
        if score < 500: return "👨‍🏫 Asistan"
        return "🧠 Profesör"


class Notification(models.Model):
    """Bildirim Modeli"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.message}"


class Contact(models.Model):
    """Destek ve İletişim Mesajları"""
    SUBJECT_CHOICES = [
        ('bug', 'Hata Bildirimi'),
        ('suggestion', 'Öneri / İstek'),
        ('copyright', 'Telif Hakkı / Şikayet'),
        ('other', 'Diğer'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"