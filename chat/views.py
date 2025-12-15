from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage
import json
import re


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
    # Regex: 0 veya 5 ile başlayan, içinde boşluk/tire olan 10-11 haneli sayılar
    digit_pattern = r'(0?5\d{2})[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
    if re.search(digit_pattern, text):
        return True

    # 2. YAZI KONTROLÜ (sıfır beş yüz..., beş yüz...)
    # "sifir bes" veya "bes yuz" kalıplarını arar.
    # \s* boşluk olsa da olmasa da yakalar (sifirbes veya sifir bes)
    text_patterns = [
        r"sifir\s*bes",  # "sıfır beş"
        r"bes\s*yuz",  # "beş yüz"
        r"sifir\s*5",  # "sıfır 5"
        r"0\s*bes"  # "0 beş"
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
            data = json.loads(request.body)
            msg = data.get('message', '').strip()

            if not msg:
                return JsonResponse({'status': 'empty'})

            # 1. Telefon Numarası Kontrolü (Rakam veya Yazı)
            if contains_phone_number(msg):
                return JsonResponse({
                    'status': 'blocked',
                    'error': 'Güvenlik nedeniyle telefon numarası (yazı veya rakamla) paylaşmak yasaktır.'
                })

            # 2. Küfür Kontrolü
            if contains_profanity(msg):
                return JsonResponse({
                    'status': 'blocked',
                    'error': 'Mesajınız uygunsuz kelimeler içeriyor.'
                })

            # ✅ Temiz mesajı kaydet
            ChatMessage.objects.create(user=request.user, message=msg)
            return JsonResponse({'status': 'ok'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})

    return JsonResponse({'status': 'error'})