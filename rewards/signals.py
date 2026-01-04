"""
Django Signals - Otomatik puan verme
Not oluşturma, güncelleme gibi işlemlerde otomatik puan verir
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notes.models import Note, Like
from rewards.gamification import (
    handle_note_created,
    handle_note_updated,
    handle_like_received,
    get_or_create_profile
)


@receiver(post_save, sender=Note)
def note_created_or_updated(sender, instance, created, **kwargs):
    """
    Not oluşturulduğunda veya güncellendiğinde çağrılır
    """
    if created:
        # Yeni not oluşturuldu
        handle_note_created(instance.user, instance)
    else:
        # Not güncellendi (sadece ilk güncellemede puan ver)
        # Spam önleme: Her güncellemede puan verme, sadece önemli güncellemelerde
        # Şimdilik her güncellemede küçük puan ver (spam önleme için düşük)
        handle_note_updated(instance.user, instance)


@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    """
    Not beğenildiğinde çağrılır
    """
    if created:
        handle_like_received(instance.note, instance.user)


@receiver(post_delete, sender=Note)
def note_deleted(sender, instance, **kwargs):
    """
    Not silindiğinde çağrılır
    İstismar önleme: Çok fazla silinen not varsa ceza verilebilir
    Şimdilik sadece istatistikleri güncelle
    """
    profile = get_or_create_profile(instance.user)
    if profile.total_notes_created > 0:
        profile.total_notes_created -= 1
        profile.save()

