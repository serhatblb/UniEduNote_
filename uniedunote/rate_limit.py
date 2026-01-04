"""
Basit rate limiting sistemi (IP ve kullanıcı bazlı)
Django cache kullanarak basit ve etkili rate limiting
"""
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from functools import wraps
import time


# Rate limit ayarları
RATE_LIMIT_CONFIG = {
    'login': {
        'limit': 5,  # 5 deneme
        'window': 60,  # 1 dakika içinde
        'key_prefix': 'rate_limit_login',
    },
    'register': {
        'limit': 3,  # 3 deneme
        'window': 3600,  # 1 saat içinde
        'key_prefix': 'rate_limit_register',
    },
    'upload': {
        'limit': 10,  # 10 yükleme
        'window': 60,  # 1 dakika içinde
        'key_prefix': 'rate_limit_upload',
    },
}


def get_client_ip(request):
    """İstemci IP adresini al"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_rate_limit(request, action_type):
    """
    Rate limit kontrolü yapar
    
    Args:
        request: Django request objesi
        action_type: 'login', 'register', 'upload'
        
    Returns:
        tuple: (is_allowed: bool, error_message: str, wait_time: int)
    """
    if action_type not in RATE_LIMIT_CONFIG:
        return True, "", 0
    
    config = RATE_LIMIT_CONFIG[action_type]
    
    # IP bazlı key
    ip = get_client_ip(request)
    ip_key = f"{config['key_prefix']}_ip_{ip}"
    
    # Kullanıcı bazlı key (eğer authenticated ise)
    user_key = None
    if request.user.is_authenticated:
        user_key = f"{config['key_prefix']}_user_{request.user.id}"
    
    # Mevcut istek sayısını al
    ip_count = cache.get(ip_key, 0)
    user_count = cache.get(user_key, 0) if user_key else 0
    
    # Limit kontrolü
    if ip_count >= config['limit'] or (user_key and user_count >= config['limit']):
        # Kalan süreyi hesapla
        ttl = cache.ttl(ip_key) or cache.ttl(user_key) or config['window']
        wait_time = max(ttl, 0)
        
        if action_type == 'login':
            error_msg = f"Çok fazla giriş denemesi. Lütfen {wait_time} saniye sonra tekrar deneyin."
        elif action_type == 'register':
            error_msg = f"Çok fazla kayıt denemesi. Lütfen {wait_time // 60} dakika sonra tekrar deneyin."
        elif action_type == 'upload':
            error_msg = f"Çok fazla dosya yükleme. Lütfen {wait_time} saniye sonra tekrar deneyin."
        else:
            error_msg = "Çok fazla istek. Lütfen bekleyin."
        
        return False, error_msg, wait_time
    
    # İsteği kaydet
    current_time = time.time()
    
    # IP için
    if ip_count == 0:
        cache.set(ip_key, 1, timeout=config['window'])
    else:
        cache.incr(ip_key)
    
    # Kullanıcı için (eğer authenticated ise)
    if user_key:
        if user_count == 0:
            cache.set(user_key, 1, timeout=config['window'])
        else:
            cache.incr(user_key)
    
    return True, "", 0


def rate_limit_decorator(action_type):
    """
    Rate limiting decorator
    
    Usage:
        @rate_limit_decorator('login')
        def login_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            is_allowed, error_msg, wait_time = check_rate_limit(request, action_type)
            
            if not is_allowed:
                # API istekleri için JSON response
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'error': error_msg,
                        'wait_time': wait_time
                    }, status=429)  # 429 Too Many Requests
                
                # Normal view'lar için messages ile hata
                from django.contrib import messages
                messages.error(request, error_msg)
                
                # Login ve register için redirect
                if action_type in ['login', 'register']:
                    from django.shortcuts import redirect
                    return redirect(request.path)
                
                # Upload için aynı sayfada kal
                return view_func(request, *args, **kwargs)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

