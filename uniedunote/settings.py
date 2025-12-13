import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv

# .env dosyasını yükle (Lokalde ve Sunucuda environment değişkenlerini okumak için)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent



# ------------------------------------------------------------------
# GÜVENLİK
# ------------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key")

# Canlıda (Sunucuda) DEBUG False olmalı, lokalde True olabilir
DEBUG = os.environ.get("DEBUG", "True") == "True"

# .env dosyasındaki ALLOWED_HOSTS'u virgülle ayırıp listeye çevirir
# Örn: "127.0.0.1,165.22.xx.xx,siteadi.com" -> ['127.0.0.1', '165.22.xx.xx', 'siteadi.com']
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

CSRF_TRUSTED_ORIGINS = []
if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):  # Render kalıntısı ama zararı yok
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}")
# Alan adın varsa HTTPS için buraya eklenmeli
if "dersnotlarım.com.tr" in str(ALLOWED_HOSTS):
    CSRF_TRUSTED_ORIGINS.append("https://dersnotlarım.com.tr")
    CSRF_TRUSTED_ORIGINS.append("https://www.dersnotlarım.com.tr")

# ------------------------------------------------------------------
# UYGULAMALAR
# ------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary SİLİNDİ (Artık sunucu diskini kullanacağız)

    "rest_framework",
    "rest_framework_simplejwt",
    "django.contrib.sites",

    # Kendi uygulamaların
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
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Statik dosyalar için performans sağlar
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
# VERİTABANI (PostgreSQL Hazır)
# ------------------------------------------------------------------
# .env dosyasındaki DATABASE_URL'i okur. Yoksa sqlite kullanır.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

AUTH_USER_MODEL = "users.User"
LANGUAGE_CODE = "tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# STATİK VE MEDYA (YEREL DİSK AYARLARI)
# ------------------------------------------------------------------

# Statik Dosyalar (CSS, JS, İkonlar)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Medya Dosyaları (Kullanıcıların yüklediği Notlar/Resimler)
# Cloudinary yerine artık sunucunun kendi klasörüne kaydedilecek.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    # Varsayılan: Yerel Disk (Media dosyaları için)
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # Statik dosyalar: WhiteNoise (Sıkıştırma yapar, hızlıdır)
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# ------------------------------------------------------------------
# MAIL AYARLARI (SMTP)
# ------------------------------------------------------------------
# .env dosyasından okur, yoksa varsayılanları kullanır
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "").strip()
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "UniEduNote <noreply@dersnotlarim.com.tr>")

# SendGrid API Key (Opsiyonel, SMTP kullanıyorsan gerek yok ama kalsın)
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")

# ------------------------------------------------------------------
# REST FRAMEWORK & JWT
# ------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

BACKEND_BASE_URL = os.environ.get("BACKEND_BASE_URL", "http://127.0.0.1:8000")