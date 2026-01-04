"""
Logging yapılandırması
Tutarlı, okunabilir ve güvenli logging sistemi
"""
import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Logs dizini oluştur
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Logging yapılandırması
# NOT: Django'nun LOGGING ayarı için dictionary
LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {funcName} {lineno} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'django.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'errors.log',
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'security.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if os.environ.get('DEBUG', 'False') == 'True' else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'uniedunote': {
            'handlers': ['file', 'error_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'uniedunote.security': {
            'handlers': ['security_file', 'error_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}


def get_logger(name='uniedunote'):
    """
    Logger instance döner
    
    Args:
        name: Logger adı (default: 'uniedunote')
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


def sanitize_log_data(data):
    """
    Log'a yazılacak verilerden hassas bilgileri temizler
    
    Args:
        data: dict veya string
        
    Returns:
        dict veya string: Temizlenmiş veri
    """
    if isinstance(data, dict):
        sensitive_keys = ['password', 'token', 'secret', 'api_key', 'access_token', 'refresh_token']
        cleaned = data.copy()
        for key in sensitive_keys:
            if key in cleaned:
                cleaned[key] = '***REDACTED***'
        return cleaned
    elif isinstance(data, str):
        # String içinde hassas bilgileri temizle
        sensitive_patterns = ['password', 'token', 'secret']
        cleaned = data
        for pattern in sensitive_patterns:
            # Basit temizleme (geliştirilebilir)
            if pattern in cleaned.lower():
                # Burada daha gelişmiş regex kullanılabilir
                pass
        return cleaned
    return data

