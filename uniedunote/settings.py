from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-q08k(z5e4fs6sglhor)k)r_(8seltdz&8io3_dj-z)lw14og@g'
DEBUG = True
ALLOWED_HOSTS = []

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
]

# ------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

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
# 💡 NOT: İş yerinde testte olduğun için mail bloklanabilir.
# Şimdilik console backend ile debug yapıyoruz:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'UniEduNote <no-reply@uniedunote.local>'

# Eğer gerçek mail göndermek istersen aşağıdakini aktif et:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'serhatblb23@gmail.com'
# EMAIL_HOST_PASSWORD = 'uygulama-şifresi-buraya'
# DEFAULT_FROM_EMAIL = 'UniEduNote <serhatblb23@gmail.com>'

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
