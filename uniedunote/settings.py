import os
from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# GÜVENLİK / ORTAM DEĞİŞKENLERİ
# ------------------------------------------------------------------
# SECRET_KEY ve DEBUG artık environment üzerinden okunuyor.
# Localde bir şey yapmana gerek yok, env yoksa default değerleri kullanır.

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-q08k(z5e4fs6sglhor)k)r_(8seltdz&8io3_dj-z)lw14og@g"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

# Render için ALLOWED_HOSTS
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF için Render domain'i
CSRF_TRUSTED_ORIGINS = []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# ------------------------------------------------------------------
# UYGULAMALAR
# ------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REST API
    'rest_framework',
    'rest_framework_simplejwt',

    # Proje uygulamaları
    'users',
    'categories',
    'notes',
    'rewards',
    'chat',
    'django.contrib.sites',
]

SITE_ID = 1

# ------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise ekleyecek olursak buraya gelir:
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uniedunote.urls'

# ------------------------------------------------------------------
# TEMPLATE AYARLARI
# ------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # templates klasörünü kullanıyoruz
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uniedunote.wsgi.application'

# ------------------------------------------------------------------
# VERİTABANI
# ------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------------------------------
# KULLANICI MODELİ
# ------------------------------------------------------------------
AUTH_USER_MODEL = 'users.User'

# ------------------------------------------------------------------
# DİL ve ZAMAN
# ------------------------------------------------------------------
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# STATİK & MEDYA
# ------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Render collectstatic buraya atacak

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Whitenoise kullanırsak (ileride istersen ekleriz):
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ------------------------------------------------------------------
# LOGIN / LOGOUT yönlendirmeleri
# ------------------------------------------------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ------------------------------------------------------------------
# GENEL
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------
# 📧 E-posta yapılandırması
# ------------------------------------------------------------------
# Prod ortamında şifreleri environment'tan okumak daha güvenli.
# Localde env set etmezsen aşağıdaki default'lar kullanılacak.

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "ai.serhat78@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "ztguqxhvaovwnhqg").strip()

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "UniEduNote <ai.serhat78@gmail.com>"
)

# ------------------------------------------------------------------
# DRF & JWT AYARLARI
# ------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ------------------------------------------------------------------
# Aktivasyon linkleri için temel backend URL
# Localde 127.0.0.1:8000, Render'da env ile değişecek
# ------------------------------------------------------------------
BACKEND_BASE_URL = os.environ.get("BACKEND_BASE_URL", "http://127.0.0.1:8000")
