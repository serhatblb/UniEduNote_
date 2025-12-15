from django.contrib.auth.models import AbstractUser
from django.db import models
from categories.models import University

class User(AbstractUser):
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)
    # email alanı zaten AbstractUser'da var ama unique yapalım
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    @property
    def rank(self):
        """Oyunlaştırma: Puanına göre rütbe getirir"""
        # Toplam puan = Yüklediği not sayısı * 10 + İndirilme sayısı
        uploads = self.note_set.count()
        downloads = sum(n.download_count for n in self.note_set.all())
        score = (uploads * 10) + downloads

        if score < 10: return "🌱 Çaylak"
        if score < 50: return "✏️ Öğrenci"
        if score < 100: return "🎓 Mezun"
        if score < 500: return "👨‍🏫 Asistan"
        return "🧠 Profesör"