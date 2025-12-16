from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage
from django.core.cache import cache
import json
import re
import time

# ==========================
# RATE LIMITING AYARLARI
# ==========================
RATE_LIMIT_CONFIG = {
    'COOLDOWN_SECONDS': 2,  # Her mesaj arası minimum süre (saniye)
    'MAX_MESSAGES': 5,  # Belirli sürede max mesaj sayısı
    'TIME_WINDOW': 10,  # Zaman penceresi (saniye)
    'BLOCK_DURATION': 30  # Limit aşımında engelleme süresi (saniye)
}


def check_rate_limit(user_id):
    """
    Gelişmiş rate limiting kontrolü
    - Basit cooldown (her mesaj arası X saniye)
    - Sliding window (Y saniyede en fazla Z mesaj)

    Returns:
        tuple: (is_allowed: bool, error_message: str, wait_time: int)
    """
    # 1. BASİT COOLDOWN KONTROLÜ
    cooldown_key = f"chat_cooldown_{user_id}"
    last_message_time = cache.get(cooldown_key)

    if last_message_time:
        elapsed = time.time() - last_message_time
        remaining = RATE_LIMIT_CONFIG['COOLDOWN_SECONDS'] - elapsed

        if remaining > 0:
            return (False, f'Biraz yavaşla kovboy! 🤠 ({int(remaining) + 1} saniye bekle)', int(remaining) + 1)

    # 2. SLIDING WINDOW KONTROLÜ (Spam koruması)
    window_key = f"chat_window_{user_id}"
    message_times = cache.get(window_key, [])

    # Eski mesajları temizle (zaman penceresi dışındakiler)
    current_time = time.time()
    message_times = [t for t in message_times if current_time - t < RATE_LIMIT_CONFIG['TIME_WINDOW']]

    # Limit kontrolü
    if len(message_times) >= RATE_LIMIT_CONFIG['MAX_MESSAGES']:
        # Kullanıcı spamcı olarak işaretle
        block_key = f"chat_blocked_{user_id}"
        cache.set(block_key, True, timeout=RATE_LIMIT_CONFIG['BLOCK_DURATION'])
        return (False, f'Çok fazla mesaj gönderdin! {RATE_LIMIT_CONFIG["BLOCK_DURATION"]} saniye engellendin. ⏰',
                RATE_LIMIT_CONFIG['BLOCK_DURATION'])

    # 3. BLOKE KONTROLÜ (Daha önce spam yaptıysa)
    block_key = f"chat_blocked_{user_id}"
    if cache.get(block_key):
        #block_ttl = cache.ttl(block_key)
        #return (False, f'Hala engellisin! Kalan süre: {block_ttl} saniye ⛔', block_ttl)
        return (False, f'Çok fazla mesaj attığın için geçici olarak engellendin! ⛔', 30)

    return (True, '', 0)


def update_rate_limit(user_id):
    """Rate limit verilerini güncelle"""
    current_time = time.time()

    # Cooldown süresini kaydet
    cooldown_key = f"chat_cooldown_{user_id}"
    cache.set(cooldown_key, current_time, timeout=RATE_LIMIT_CONFIG['COOLDOWN_SECONDS'])

    # Sliding window'a ekle
    window_key = f"chat_window_{user_id}"
    message_times = cache.get(window_key, [])
    message_times.append(current_time)
    cache.set(window_key, message_times, timeout=RATE_LIMIT_CONFIG['TIME_WINDOW'])


# ==========================
# CHAT SAYFASI
# ==========================
@login_required(login_url='/login/')
def chat_room(request):
    return render(request, 'chat/room.html')


@login_required
def get_messages(request):
    messages = ChatMessage.objects.all().order_by('-created_at')[:50]
    data = [{
        'user': m.user.username,
        'avatar_url': m.user.avatar.url if m.user.avatar else None,
        'message': m.message,
        'created_at': m.created_at.strftime('%H:%M')
    } for m in reversed(messages)]
    return JsonResponse({'messages': data})


# ==========================
# FİLTRELER
# ==========================
BAD_WORDS = [
    "aptal", "salak", "gerizekalı", "geri zekalı", "embesil", "ahmak",
    "beyinsiz", "mal", "dangoz", "öküz", "eşek", "hayvan",
    "şerefsiz", "namussuz", "adi", "alçak", "pislik", "rezil",
    "iğrenç", "terbiyesiz",
    "orospu", "oç", "oc", "kahpe", "sürtük",
    "fahişe", "pezevenk", "ibne", "top", "gavat", "puşt",
    "yavşak", "dangalak",
    "amk", "aq", "amına", "sikeyim", "sikim", "siktir",
    "sik", "sikik", "yarrak", "yarak", "taşak", "göt", "götveren",
    "bok", "boktan",
    "piç", "piç kurusu", "it", "köpek", "çakal", "hödük",
    "keko", "maganda", "ezik",
    "geber", "defol", "kes sesini",
    "am", "amcık", "amcik", "godoş", "ibnelik"
]


def normalize_text(text):
    """Türkçe karakterleri İngilizce karşılıklarına çevirir"""
    replacements = {
        "ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g",
        "ç": "c", "Ç": "c", "ö": "o", "Ö": "o", "ü": "u", "Ü": "u"
    }
    text = text.lower()
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def contains_profanity(text):
    normalized_text = normalize_text(text)
    for bad_word in BAD_WORDS:
        normalized_bad_word = normalize_text(bad_word)
        if normalized_bad_word in normalized_text:
            return True
    return False


def contains_phone_number(text):
    """
    Hem rakam hem de yazı ile yazılan telefon numaralarını yakalar.
    """
    normalized = normalize_text(text)

    # 1. RAKAM KONTROLÜ (0532... veya 532...)
    digit_pattern = r'(0?5\d{2})[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
    if re.search(digit_pattern, text):
        return True

    # 2. YAZI KONTROLÜ (sıfır beş yüz..., beş yüz...)
    text_patterns = [
        r"sifir\s*bes",
        r"bes\s*yuz",
        r"sifir\s*5",
        r"0\s*bes"
    ]

    for p in text_patterns:
        if re.search(p, normalized):
            return True

    return False


# ==========================
# MESAJ GÖNDERME
# ==========================
@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            user_id = request.user.id

            # RATE LIMIT KONTROLÜ
            is_allowed, error_msg, wait_time = check_rate_limit(user_id)
            if not is_allowed:
                return JsonResponse({
                    'status': 'blocked',
                    'error': error_msg,
                    'wait_time': wait_time
                })

            data = json.loads(request.body)
            msg = data.get('message', '').strip()

            if not msg:
                return JsonResponse({'status': 'empty'})

            # Filtreler (Telefon ve Küfür)
            if contains_phone_number(msg):
                return JsonResponse({
                    'status': 'blocked',
                    'error': 'Telefon numarası paylaşmak yasaktır. 📵'
                })

            if contains_profanity(msg):
                return JsonResponse({
                    'status': 'blocked',
                    'error': 'Uygunsuz içerik tespit edildi. 🚫'
                })

            # Mesajı kaydet
            ChatMessage.objects.create(user=request.user, message=msg)

            # Rate limit verilerini güncelle
            update_rate_limit(user_id)

            return JsonResponse({'status': 'ok'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})

    return JsonResponse({'status': 'error'})