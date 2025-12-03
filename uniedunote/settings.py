import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

# Proje ana dizini
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# GÜVENLİK VE ORTAM AYARLARI
# ------------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-gizli-anahtar-yoksa-bunu-kullan")

# Canlıda DEBUG False olmalı, Render environment'tan çekiyoruz
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Render'ın verdiği domaini otomatik ekle
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# ------------------------------------------------------------------
# UYGULAMALAR (APPS)
# ------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    # 3. Parti Kütüphaneler (Sıralama Önemli)
    'cloudinary_storage',  # staticfiles'dan ÖNCE olmalı
    "django.contrib.staticfiles",
    'cloudinary',
    "rest_framework",
    "rest_framework_simplejwt",
    "django.contrib.sites",

    # Senin Uygulamaların
    "users",
    "categories",
    "notes",
    "rewards",
    "chat",
]

SITE_ID = 1

# ------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <-- WhiteNoise burada olmalı
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "uniedunote.urls"

# ------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "uniedunote.wsgi.application"

# ------------------------------------------------------------------
# VERİTABANI
# ------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        # Render'da DATABASE_URL varsa Postgres kullanır, yoksa SQLite
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# ------------------------------------------------------------------
# KULLANICI MODELİ VE DİL
# ------------------------------------------------------------------
AUTH_USER_MODEL = "users.User"
LANGUAGE_CODE = "tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# CLOUDINARY AYARLARI
# ------------------------------------------------------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# ------------------------------------------------------------------
# STORAGE AYARLARI (HEM YENİ HEM ESKİ SİSTEM - ÇAKIŞMA OLMASIN DİYE)
# ------------------------------------------------------------------

# 1. Yeni Nesil Django 5 Ayarı (Django bunu kullanır)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# 2. Eski Nesil Ayarlar (Kütüphaneler hata vermesin diye bunları da ekliyoruz)
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ------------------------------------------------------------------
# URL VE PATH AYARLARI
# ------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ------------------------------------------------------------------
# LOGIN / LOGOUT YÖNLENDİRMELERİ
# ------------------------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# ------------------------------------------------------------------
# GENEL VE E-POSTA AYARLARI
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "ai.serhat78@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "").strip()
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "UniEduNote <ai.serhat78@gmail.com>")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")

# ------------------------------------------------------------------
# DRF & JWT
# ------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

BACKEND_BASE_URL = os.environ.get("BACKEND_BASE_URL", "http://127.0.0.1:8000")