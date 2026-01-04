"""
Gamification Sistemi - Puan Hesaplama ve İşleme Mantığı

Bu modül, kullanıcıların puan kazanması, seviye atlaması ve 
istismar önleme mekanizmalarını yönetir.
"""

from django.db import transaction
from django.utils import timezone
from datetime import timedelta, date
from rewards.models import UserProfile, PointTransaction, Badge

# Note ve Like modelleri signal'larda kullanılacak, burada import etmeye gerek yok


# ============================================
# PUAN SİSTEMİ - AKSİYON BAZLI PUANLAR
# ============================================

POINT_VALUES = {
    'note_created': 50,          # Not oluşturma (ilk yükleme)
    'note_updated': 5,           # Not güncelleme (spam önleme için düşük)
    'like_received': 2,          # Her beğeni için
    'download_received': 1,      # Her indirme için
    'favorite_received': 3,      # Favoriye eklenme (henüz favori sistemi yok, ileride)
    'profile_completed': 20,     # Profil tamamlama (tek seferlik)
    'daily_login': 5,            # Günlük giriş (günde bir kez)
}

# İSTİSMAR ÖNLEME LİMİTLERİ
DAILY_NOTE_LIMIT = 10           # Günde maksimum not oluşturma
MIN_NOTE_QUALITY_SCORE = 0.1    # Minimum kalite skoru (silinen notlar için)


def get_or_create_profile(user):
    """Kullanıcı profili yoksa oluştur"""
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


def add_points(user, transaction_type, points, description='', note=None):
    """
    Kullanıcıya puan ekler ve transaction loglar
    
    Args:
        user: User objesi
        transaction_type: PointTransaction.TRANSACTION_TYPES'den biri
        points: Eklenecek puan (negatif olabilir)
        description: Açıklama
        note: İlişkili Note objesi (opsiyonel)
    """
    with transaction.atomic():
        profile = get_or_create_profile(user)
        
        # Puan ekle
        profile.total_xp += points
        
        # Seviyeyi güncelle
        new_level = profile.calculate_level()
        level_up = new_level > profile.level
        profile.level = new_level
        
        profile.save()
        
        # Transaction log
        PointTransaction.objects.create(
            user=user,
            transaction_type=transaction_type,
            points=points,
            description=description,
            note=note
        )
        
        # Seviye atlama kontrolü
        if level_up:
            check_level_badges(user, new_level)
            # Bildirim gönderilebilir (ileride)
        
        return profile


def handle_note_created(user, note):
    """
    Not oluşturulduğunda çağrılır
    İstismar kontrolü yapar ve puan verir
    """
    profile = get_or_create_profile(user)
    today = timezone.now().date()
    
    # Günlük limit kontrolü
    if profile.last_note_date == today:
        if profile.notes_created_today >= DAILY_NOTE_LIMIT:
            # Günlük limit aşıldı - puan verilmez
            return profile, False, "Günlük not limiti aşıldı (10 not/gün)"
    else:
        # Yeni gün, sayacı sıfırla
        profile.notes_created_today = 0
        profile.last_note_date = today
    
    # Puan ver
    profile.notes_created_today += 1
    profile.total_notes_created += 1
    profile.save()
    
    add_points(
        user=user,
        transaction_type='note_created',
        points=POINT_VALUES['note_created'],
        description=f"Not oluşturuldu: {note.title}",
        note=note
    )
    
    # İlk not rozeti kontrolü
    if profile.total_notes_created == 1:
        award_badge(user, 'first_note')
    
    # Not sayısı rozetleri
    check_note_count_badges(user, profile.total_notes_created)
    
    return profile, True, "Puan kazanıldı"


def handle_note_updated(user, note):
    """
    Not güncellendiğinde çağrılır
    Spam önleme için düşük puan verir
    """
    add_points(
        user=user,
        transaction_type='note_updated',
        points=POINT_VALUES['note_updated'],
        description=f"Not güncellendi: {note.title}",
        note=note
    )
    return True


def handle_like_received(note, liked_by_user):
    """
    Not beğenildiğinde çağrılır
    Not sahibine puan verir (kendi beğenisi sayılmaz)
    """
    from notes.models import Like
    
    note_owner = note.user
    
    # Kendi notunu beğenme kontrolü
    if note_owner == liked_by_user:
        return False, "Kendi notunu beğenemezsin"
    
    # Aynı kullanıcıdan tekrar beğeni kontrolü (Like modelinde unique_together var ama yine de kontrol)
    if Like.objects.filter(user=liked_by_user, note=note).exists():
        return False, "Bu notu zaten beğendin"
    
    # Puan ver
    profile = get_or_create_profile(note_owner)
    profile.total_likes_received += 1
    profile.save()
    
    add_points(
        user=note_owner,
        transaction_type='like_received',
        points=POINT_VALUES['like_received'],
        description=f"Not beğenildi: {note.title}",
        note=note
    )
    
    # İlk beğeni rozeti
    if profile.total_likes_received == 1:
        award_badge(note_owner, 'first_like')
    
    # 100 beğeni rozeti
    if profile.total_likes_received == 100:
        award_badge(note_owner, 'likes_100')
    
    return True, "Puan kazanıldı"


def handle_download_received(note, downloaded_by_user):
    """
    Not indirildiğinde çağrılır
    Not sahibine puan verir (kendi indirmesi sayılmaz)
    """
    note_owner = note.user
    
    # Kendi notunu indirme kontrolü
    if note_owner == downloaded_by_user:
        return False, "Kendi notunu indiremezsin (puan için)"
    
    # Puan ver
    profile = get_or_create_profile(note_owner)
    profile.total_downloads_received += 1
    profile.save()
    
    add_points(
        user=note_owner,
        transaction_type='download_received',
        points=POINT_VALUES['download_received'],
        description=f"Not indirildi: {note.title}",
        note=note
    )
    
    # İlk indirme rozeti
    if profile.total_downloads_received == 1:
        award_badge(note_owner, 'first_download')
    
    # 1000 indirme rozeti
    if profile.total_downloads_received == 1000:
        award_badge(note_owner, 'downloads_1000')
    
    return True, "Puan kazanıldı"


def handle_daily_login(user):
    """
    Günlük giriş puanı verir
    Günde bir kez puan verir, seri takibi yapar
    """
    profile = get_or_create_profile(user)
    today = timezone.now().date()
    
    # Bugün zaten puan verildi mi?
    if profile.last_daily_login == today:
        return False, "Bugün zaten giriş puanı aldın"
    
    # Seri kontrolü
    yesterday = today - timedelta(days=1)
    if profile.last_daily_login == yesterday:
        # Seri devam ediyor
        profile.daily_login_streak += 1
    elif profile.last_daily_login is None or profile.last_daily_login < yesterday:
        # Seri kırıldı, sıfırla
        profile.daily_login_streak = 1
    
    profile.last_daily_login = today
    profile.save()
    
    add_points(
        user=user,
        transaction_type='daily_login',
        points=POINT_VALUES['daily_login'],
        description="Günlük giriş puanı"
    )
    
    # Seri rozetleri
    if profile.daily_login_streak == 7:
        award_badge(user, 'daily_streak_7')
    elif profile.daily_login_streak == 30:
        award_badge(user, 'daily_streak_30')
    
    return True, f"Günlük giriş puanı! Seri: {profile.daily_login_streak} gün"


def handle_profile_completed(user):
    """
    Profil tamamlandığında çağrılır
    Tek seferlik puan verir
    """
    profile = get_or_create_profile(user)
    
    if profile.profile_completed:
        return False, "Profil zaten tamamlanmış"
    
    # Profil tamamlanma kontrolü
    if user.university and user.avatar:
        profile.profile_completed = True
        profile.save()
        
        add_points(
            user=user,
            transaction_type='profile_completed',
            points=POINT_VALUES['profile_completed'],
            description="Profil tamamlandı"
        )
        
        return True, "Profil tamamlama puanı kazanıldı"
    
    return False, "Profil henüz tamamlanmamış"


# ============================================
# ROZET SİSTEMİ
# ============================================

def award_badge(user, badge_type):
    """Kullanıcıya rozet verir (eğer yoksa)"""
    badge, created = Badge.objects.get_or_create(
        user=user,
        badge_type=badge_type
    )
    return created


def check_level_badges(user, level):
    """Seviye rozetlerini kontrol eder"""
    if level == 5:
        award_badge(user, 'level_5')
    elif level == 10:
        award_badge(user, 'level_10')


def check_note_count_badges(user, note_count):
    """Not sayısı rozetlerini kontrol eder"""
    if note_count == 10:
        award_badge(user, 'notes_10')
    elif note_count == 50:
        award_badge(user, 'notes_50')
    elif note_count == 100:
        award_badge(user, 'notes_100')


# ============================================
# LİDERLİK TABLOSU
# ============================================

def get_leaderboard(limit=10, period=None):
    """
    Liderlik tablosunu döndürür
    
    Args:
        limit: Kaç kullanıcı döndürülecek
        period: 'daily', 'weekly', 'monthly' veya None (tüm zamanlar)
    """
    queryset = UserProfile.objects.select_related('user').all()
    
    if period == 'daily':
        today = timezone.now().date()
        queryset = queryset.filter(
            point_transactions__created_at__date=today
        ).annotate(
            daily_xp=Sum('point_transactions__points')
        ).order_by('-daily_xp')[:limit]
    elif period == 'weekly':
        week_ago = timezone.now() - timedelta(days=7)
        queryset = queryset.filter(
            point_transactions__created_at__gte=week_ago
        ).annotate(
            weekly_xp=Sum('point_transactions__points')
        ).order_by('-weekly_xp')[:limit]
    elif period == 'monthly':
        month_ago = timezone.now() - timedelta(days=30)
        queryset = queryset.filter(
            point_transactions__created_at__gte=month_ago
        ).annotate(
            monthly_xp=Sum('point_transactions__points')
        ).order_by('-monthly_xp')[:limit]
    else:
        # Tüm zamanlar
        queryset = queryset.order_by('-total_xp', '-level')[:limit]
    
    return queryset

