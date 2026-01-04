from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from users.models import User


class UserProfile(models.Model):
    """
    Kullanıcının oyunlaştırma profili
    XP (Experience Points) ve Level bilgilerini tutar
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gamification_profile')
    
    # Puan ve Seviye
    total_xp = models.IntegerField(default=0, db_index=True)  # Toplam deneyim puanı
    level = models.IntegerField(default=1, db_index=True)  # Mevcut seviye
    
    # İstatistikler
    total_notes_created = models.IntegerField(default=0)  # Toplam oluşturulan not sayısı
    total_likes_received = models.IntegerField(default=0)  # Toplam alınan beğeni
    total_downloads_received = models.IntegerField(default=0)  # Toplam alınan indirme
    
    # Günlük takip
    last_daily_login = models.DateField(null=True, blank=True)  # Son günlük giriş tarihi
    daily_login_streak = models.IntegerField(default=0)  # Günlük giriş serisi
    
    # Profil tamamlama
    profile_completed = models.BooleanField(default=False)  # Profil tamamlandı mı?
    
    # İstismar önleme
    notes_created_today = models.IntegerField(default=0)  # Bugün oluşturulan not sayısı
    last_note_date = models.DateField(null=True, blank=True)  # Son not oluşturma tarihi
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_xp']  # Liderlik tablosu için
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level} ({self.total_xp} XP)"
    
    def calculate_level(self):
        """
        Toplam XP'ye göre seviyeyi hesaplar
        Exponential growth: Her seviye bir öncekinden %50 daha zor
        Level 1→2: 100 XP
        Level 2→3: 150 XP
        Level 3→4: 225 XP
        Level 4→5: 337 XP
        ...
        """
        if self.total_xp < 100:
            return 1
        
        level = 1
        required_xp = 100  # Level 1→2 için gerekli XP
        current_xp = self.total_xp
        
        while current_xp >= required_xp:
            level += 1
            current_xp -= required_xp
            required_xp = int(required_xp * 1.5)  # Her seviye %50 daha zor
        
        return level
    
    def get_xp_for_next_level(self):
        """Bir sonraki seviyeye geçmek için gereken toplam XP"""
        if self.level == 1:
            return 100
        
        # Mevcut seviyeye kadar gereken XP'yi hesapla
        total_required = 0
        required_xp = 100
        
        for lvl in range(1, self.level + 1):
            total_required += required_xp
            required_xp = int(required_xp * 1.5)
        
        return total_required
    
    def get_xp_progress(self):
        """
        Mevcut seviye için ilerleme bilgisi
        Returns: (current_xp_in_level, required_xp_for_level, percentage)
        """
        if self.level == 1:
            current_in_level = self.total_xp
            required = 100
        else:
            # Önceki seviyelere kadar gereken XP
            total_previous = 0
            required_xp = 100
            for lvl in range(1, self.level):
                total_previous += required_xp
                required_xp = int(required_xp * 1.5)
            
            # Mevcut seviye için gereken XP
            current_in_level = self.total_xp - total_previous
            required = required_xp
        
        percentage = min(100, int((current_in_level / required) * 100)) if required > 0 else 100
        
        return {
            'current': current_in_level,
            'required': required,
            'percentage': percentage,
            'remaining': max(0, required - current_in_level)
        }
    
    def get_level_badge(self):
        """Seviyeye göre rozet/ikon döndürür"""
        badges = {
            1: {'icon': '🌱', 'name': 'Çaylak', 'color': '#95a5a6'},
            2: {'icon': '📚', 'name': 'Öğrenci', 'color': '#3498db'},
            3: {'icon': '🎓', 'name': 'Mezun', 'color': '#2ecc71'},
            4: {'icon': '👨‍🏫', 'name': 'Asistan', 'color': '#9b59b6'},
            5: {'icon': '🧠', 'name': 'Profesör', 'color': '#f39c12'},
            6: {'icon': '👑', 'name': 'Dekan', 'color': '#e74c3c'},
            7: {'icon': '🌟', 'name': 'Rektör', 'color': '#e67e22'},
            8: {'icon': '💎', 'name': 'Efsane', 'color': '#1abc9c'},
        }
        
        # Level 8'den sonra her 5 seviyede bir özel rozet
        if self.level >= 8:
            badge = badges[8].copy()
            badge['name'] = f"Efsane {self.level}"
            return badge
        
        return badges.get(self.level, badges[8])


class PointTransaction(models.Model):
    """
    Puan hareketlerini loglar
    Her puan kazanma/ceza işlemi burada kaydedilir
    """
    TRANSACTION_TYPES = [
        ('note_created', 'Not Oluşturma'),
        ('note_updated', 'Not Güncelleme'),
        ('like_received', 'Beğeni Alınması'),
        ('download_received', 'İndirme Alınması'),
        ('favorite_received', 'Favoriye Eklenme'),
        ('profile_completed', 'Profil Tamamlama'),
        ('daily_login', 'Günlük Giriş'),
        ('penalty_spam', 'Spam Cezası'),
        ('penalty_low_quality', 'Düşük Kalite Cezası'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_transactions')
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    points = models.IntegerField()  # Pozitif veya negatif olabilir
    description = models.CharField(max_length=255, blank=True)
    
    # İlişkili nesne (opsiyonel)
    note = models.ForeignKey('notes.Note', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['transaction_type', '-created_at']),
        ]
    
    def __str__(self):
        sign = '+' if self.points > 0 else ''
        return f"{self.user.username}: {sign}{self.points} XP ({self.get_transaction_type_display()})"


class Badge(models.Model):
    """
    Rozet/Achievement sistemi (ileride genişletilebilir)
    """
    BADGE_TYPES = [
        ('first_note', 'İlk Not'),
        ('first_like', 'İlk Beğeni'),
        ('first_download', 'İlk İndirme'),
        ('notes_10', '10 Not'),
        ('notes_50', '50 Not'),
        ('notes_100', '100 Not'),
        ('likes_100', '100 Beğeni'),
        ('downloads_1000', '1000 İndirme'),
        ('level_5', 'Seviye 5'),
        ('level_10', 'Seviye 10'),
        ('daily_streak_7', '7 Gün Seri'),
        ('daily_streak_30', '30 Gün Seri'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge_type = models.CharField(max_length=30, choices=BADGE_TYPES, unique=True)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge_type')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_badge_type_display()}"
