from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage
import json
import re

# ==========================
# CHAT VIEWS
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
# KÜFÜR FİLTRESİ
# ==========================

BAD_WORDS = [
    "aptal", "salak", "gerizekalı", "geri zekalı", "embesil", "ahmak",
    "beyinsiz", "mal", "dangoz", "öküz", "eşek", "hayvan",
    "şerefsiz", "namussuz", "adi", "alçak", "pislik", "rezil",
    "iğrenç", "terbiyesiz",

    "orospu", "orospu çocuğu", "oç", "oc", "kahpe", "sürtük",
    "fahişe", "pezevenk", "ibne", "top", "gavat", "puşt",
    "yavşak", "dangalak",

    "amk", "aq", "amına koy", "amına koyayım", "amına koyim",
    "ananı sik", "anasını sik", "sikeyim", "sikim", "siktir",

    "sik", "sikik", "yarrak", "yarak", "taşak", "göt", "götveren",
    "bok", "boktan",

    "piç", "piç kurusu", "it", "köpek", "çakal", "hödük",
    "keko", "maganda", "ezik",

    "geber", "defol", "kes sesini",

    "am", "amcık", "amcik", "amına",

    "godoş", "ibnelik"
]


def normalize_text(text):
    replacements = {
        "ı": "i", "İ": "i",
        "ş": "s", "Ş": "s",
        "ğ": "g", "Ğ": "g",
        "ç": "c", "Ç": "c",
        "ö": "o", "Ö": "o",
        "ü": "u", "Ü": "u"
    }
    text = text.lower()
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def word_to_regex(word):
    word = normalize_text(word)
    pattern = ""
    for char in word:
        pattern += char + r"[\W_]*"
    return pattern


def filter_profanity(text):
    normalized = normalize_text(text)

    for bad_word in BAD_WORDS:
        pattern = word_to_regex(bad_word)
        regex = re.compile(pattern, re.IGNORECASE)

        if regex.search(normalized):
            text = regex.sub("*" * len(bad_word), text)

    return text


def contains_profanity(text):
    normalized = normalize_text(text)

    for bad_word in BAD_WORDS:
        pattern = word_to_regex(bad_word)
        if re.search(pattern, normalized, re.IGNORECASE):
            return True
    return False


# ==========================
# MESAJ GÖNDERME
# ==========================

@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        msg = data.get('message', '').strip()

        if not msg:
            return JsonResponse({'status': 'empty'})

        # 🚫 Küfür varsa engelle
        if contains_profanity(msg):
            return JsonResponse({
                'status': 'blocked',
                'error': 'Mesajınız uygunsuz kelimeler içeriyor.'
            })

        # ✅ Temiz mesajı kaydet
        ChatMessage.objects.create(
            user=request.user,
            message=msg
        )

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})
