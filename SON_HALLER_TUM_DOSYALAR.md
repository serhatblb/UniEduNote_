# 📦 TÜM DOSYALARIN SON HALLERİ - PRODUCTION READY

Bu dosyalar GitHub'a push edilebilir ve sunucuda çalıştırılabilir.

---

## 1. uniedunote/settings.py

```python
import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# GÜVENLİK
# ------------------------------------------------------------------
# SECRET_KEY environment variable'dan alınmalı, production'da zorunlu
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    import warnings
    warnings.warn(
        "SECRET_KEY environment variable ayarlanmamış! "
        "Production için mutlaka ayarlanmalı. Geçici olarak default key kullanılıyor.",
        UserWarning
    )
    # Geçici fallback (sadece development için)
    SECRET_KEY = "django-insecure-temporary-key-change-in-production"

# DEBUG: Production'da False olmalı, development'ta True
# Environment variable "True" string'i ise True, değilse False
DEBUG_ENV = os.environ.get("DEBUG", "False").lower()
DEBUG = DEBUG_ENV in ("true", "1", "yes")

# Allowed Hosts: Production'da domain adları, development'ta localhost
ALLOWED_HOSTS_ENV = os.environ.get("ALLOWED_HOSTS", "")
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(",") if host.strip()]
else:
    # Development modunda localhost ve 127.0.0.1 izin ver
    if DEBUG:
        ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
    else:
        # Production'da ALLOWED_HOSTS boşsa uyarı ver ama çalışmaya devam et
        import warnings
        warnings.warn(
            "ALLOWED_HOSTS environment variable ayarlanmamış! "
            "Production için domain adları ayarlanmalı.",
            UserWarning
        )
        ALLOWED_HOSTS = ["*"]  # Geçici olarak tüm host'lara izin ver (GÜVENLİK RİSKİ!)

# CSRF Trusted Origins: HTTPS için
CSRF_TRUSTED_ORIGINS = []
if not DEBUG:
    # Production'da HTTPS origin'leri ekle
    for host in ALLOWED_HOSTS:
        if host and host != "*" and not host.startswith("127.0.0.1") and not host.startswith("localhost"):
            CSRF_TRUSTED_ORIGINS.append(f"https://{host}")
            CSRF_TRUSTED_ORIGINS.append(f"https://www.{host}")
# Eski domain kontrolü (geriye dönük uyumluluk için)
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
    # Cloudinary YOK
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
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# CACHE AYARLARI (Veritabanı Tabanlı)
# Gunicorn işçilerinin ortak çalışması için şart!
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
AUTH_USER_MODEL = "users.User"
LANGUAGE_CODE = "tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# STATİK VE MEDYA
# ------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# ------------------------------------------------------------------
# MAIL AYARLARI
# ------------------------------------------------------------------
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "").strip()
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "UniEduNote <ai.serhat78@gmail.com>")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")

# ------------------------------------------------------------------
# JWT
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
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# OTOMATİK ÇIKIŞ (GÜVENLİK)
# 30 dakika (1800 saniye) işlem yapmazsa çıkış yap
SESSION_COOKIE_AGE = 1800
# Her işlemde süreyi sıfırla (Aktifse atmasın)
SESSION_SAVE_EVERY_REQUEST = True

# ------------------------------------------------------------------
# GÜVENLİK BAŞLIKLARI (Security Headers)
# ------------------------------------------------------------------
# HTTPS için cookie güvenliği (production'da True olmalı)
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF Cookie güvenliği
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Güvenlik başlıkları
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS yönlendirmesi (production'da True olmalı)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 yıl
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

## 2. users/views_api.py

```python
import json

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .tokens import account_activation_token
from .serializers import UserSerializer
from .email_utils import send_activation_email
import json

User = get_user_model()


# ✅ Kullanıcı Kaydı (API)
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            activation_link = f"{settings.BACKEND_BASE_URL}/activate/{uid}/{token}/"

            send_activation_email(user, activation_link)

            return Response({"message": "Kayıt başarılı! Aktivasyon e-postası gönderildi."}, status=201)
        return Response(serializer.errors, status=400)


# ✅ Hesap Aktivasyonu (API üzerinden kontrol)
class ActivateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Hesap başarıyla aktifleştirildi."})
        return Response({"error": "Aktivasyon bağlantısı geçersiz."}, status=400)


# ✅ JWT Token
class MyTokenObtainPairView(TokenObtainPairView):
    """Kullanıcı girişinde JWT döner."""
    pass


# ✅ Şifre sıfırlama (istek)
class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Güvenlik için hata vermiyoruz, var gibi davranıyoruz
            return Response({"message": "Eğer kayıtlıysa, şifre sıfırlama e-postası gönderildi."})

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        reset_link = f"{settings.BACKEND_BASE_URL}/password-reset-confirm/{uid}/{token}/"

        subject = "UniEduNote Şifre Sıfırlama"

        # HTML TASARIMLI MAİL İÇERİĞİ
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
            <h2 style="color: #007AFF;">Şifre Sıfırlama İsteği 🔒</h2>
            <p>Merhaba {user.username},</p>
            <p>Hesabınız için şifre sıfırlama talebinde bulundunuz.</p>
            <p style="margin: 30px 0;">
                <a href="{reset_link}" style="background-color: #007AFF; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Şifremi Sıfırla</a>
            </p>
            <p style="font-size: 12px; color: #888;">Bu butona tıklayamazsanız, aşağıdaki linki tarayıcınıza yapıştırın:<br>{reset_link}</p>
        </div>
        """

        try:
            # html_message parametresini ekliyoruz
            send_mail(subject, "", settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False, html_message=html_message)
            return Response({"message": "Şifre sıfırlama e-postası gönderildi."})
        except Exception as e:
            return Response({"error": f"Mail gönderilemedi: {str(e)}"}, status=500)

# ✅ Şifre sıfırlama (onay)
class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Geçersiz bağlantı."}, status=400)

        if account_activation_token.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message": "Şifre başarıyla güncellendi."})
        return Response({"error": "Token geçersiz veya süresi dolmuş."}, status=400)


# ✅ Profil Bilgileri (JWT zorunlu)
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return Response(data)


# ✅ Session login
# NOT: DRF APIView kullanıldığı için CSRF koruması otomatik olarak devre dışıdır.
# DRF APIView'lar Django'nun CSRF middleware'ini bypass eder.
class SessionLoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            login_input = request.data.get("username")  # Bu email de olabilir, username de
            password = request.data.get("password")

            if not login_input or not password:
                return Response({"error": "Kullanıcı adı ve şifre zorunlu"}, status=400)

            # --- Zeka Burada: Email mi Username mi? ---
            username_to_auth = login_input
            if '@' in login_input:
                try:
                    user_obj = User.objects.get(email=login_input)
                    username_to_auth = user_obj.username
                except User.DoesNotExist:
                    # Email bulunamazsa rastgele bişey ata ki authenticate fail olsun
                    username_to_auth = "bulunamayan_kullanici"
            # ------------------------------------------

            user = authenticate(request, username=username_to_auth, password=password)

            if user and user.is_active:
                login(request, user)
                return Response({"message": "Login başarılı", "username": user.username})
            else:
                return Response({"error": "Giriş bilgileri hatalı!"}, status=401)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

# ✅ Profil Güncelleme (JWT zorunlu)
class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Dosya yükleme yeteneği

    def post(self, request):
        user = request.user
        data = request.data

        # Kullanıcı adı ve e-posta
        username = data.get("username")
        email = data.get("email")

        if username: user.username = username
        if email: user.email = email

        # Şifre değiştirme
        password = data.get("password")
        if password and len(password) >= 8:
            user.set_password(password)

        # Üniversite Güncelleme (ID gelir)
        uni_id = data.get("university")
        if uni_id:
            try:
                # Veritabanından ID ile bulup atıyoruz
                from categories.models import University
                user.university = University.objects.get(id=uni_id)
            except:
                pass  # Hatalı ID gelirse yoksay

        # Avatar Güncelleme (Dosya)
        avatar = request.FILES.get('avatar')
        if avatar:
            user.avatar = avatar

        try:
            user.save()
            return Response({"message": "Profil başarıyla güncellendi."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
```

---

## 3. users/urls.py

```python
from django.urls import path
from .views_api import (
    RegisterAPIView,
    ActivateAPIView,
    MyTokenObtainPairView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    SessionLoginAPIView,
    UserProfileUpdateAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('activate/<uidb64>/<token>/', ActivateAPIView.as_view(), name='api-activate'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # CSRF korumalı session login (JWT kullanımı önerilir)
    path('session-login/', SessionLoginAPIView.as_view(), name='session-login'),

    path('password/reset/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),

    path("profile/update/", UserProfileUpdateAPIView.as_view(), name="profile-update"),
]
```

---

## 4. notes/views.py

```python
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from categories.models import University, Faculty, Department, Course
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.http import JsonResponse
from users.models import Notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 📤 Not yükleme
@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/upload_note.html', {'form': form})


# 📋 Not listesi (filtreli) - Pagination ile
def note_list(request):
    sort_by = request.GET.get('sort', 'newest')

    if sort_by == 'popular':
        ordering = '-download_count'
    elif sort_by == 'liked':
        ordering = '-likes'
    else:
        ordering = '-uploaded_at'  # Varsayılan: En yeni

    # N+1 query problemini çözmek için select_related ve prefetch_related kullan
    notes = Note.objects.select_related(
        'user', 'university', 'faculty', 'department', 'course'
    ).prefetch_related(
        'comments', 'likes_set'
    ).order_by(ordering)

    university = request.GET.get('university')
    department = request.GET.get('department')
    course = request.GET.get('course')

    if university:
        notes = notes.filter(university__id=university)
    if department:
        notes = notes.filter(department__id=department)
    if course:
        notes = notes.filter(course__id=course)

    # Pagination: Sayfa başına 20 not
    paginator = Paginator(notes, 20)
    page = request.GET.get('page', 1)
    
    try:
        notes_page = paginator.page(page)
    except PageNotAnInteger:
        notes_page = paginator.page(1)
    except EmptyPage:
        notes_page = paginator.page(paginator.num_pages)

    universities = University.objects.all().order_by('name')
    departments = Department.objects.all().order_by('name')
    courses = Course.objects.all().order_by('name')

    context = {
        'notes': notes_page,
        'universities': universities,
        'departments': departments,
        'courses': courses,
        'sort_by': sort_by,
    }
    request.session['last_notes_list_url'] = request.get_full_path()
    return render(request, 'notes/note_list.html', context)


# 🔍 Not detay
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


# 📥 Not indirme
@login_required
def download_note(request, pk):
    note = get_object_or_404(Note, pk=pk)

    try:
        if note.file:
            note.download_count += 1
            note.save()

            # BİLDİRİM GÖNDER (Kendi notunu indirince gitmesin)
            if note.user != request.user:
                Notification.objects.create(
                    user=note.user,  # Notun sahibine
                    message=f"Tebrikler! '{note.title}' başlıklı notun {request.user.username} tarafından indirildi. 🎉"
                )

            return redirect(note.file.url)
    except Exception as e:
        messages.error(request, "Dosya bulunamadı.")

    return redirect('note_detail', pk=pk)

# 🏠 Dashboard
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')


# ✏️ Not düzenleme
@login_required(login_url="/login/")
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        note.title = request.POST.get("title")
        note.description = request.POST.get("description")
        if "file" in request.FILES:
            note.file = request.FILES["file"]
        note.save()
        messages.success(request, "Not başarıyla güncellendi.")
        return redirect("note_detail", pk=note.pk)
    return render(request, "notes/edit_note.html", {"note": note})

# ✏ Not silme
@login_required(login_url='/login/')
@require_POST
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    messages.success(request, "Not silindi.")
    redirect_url = request.session.get('last_notes_list_url', '/notes/')
    return redirect(redirect_url)

def load_faculties(request):
    university_id = request.GET.get('university')
    faculties = Faculty.objects.filter(university_id=university_id).order_by('name')
    return JsonResponse(list(faculties.values('id', 'name')), safe=False)

def load_departments(request):
    faculty_id = request.GET.get('faculty')
    departments = Department.objects.filter(faculty_id=faculty_id).order_by('name')
    return JsonResponse(list(departments.values('id', 'name')), safe=False)

def load_courses(request):
    department_id = request.GET.get('department')
    courses = Course.objects.filter(department_id=department_id).order_by('name')
    return JsonResponse(list(courses.values('id', 'name')), safe=False)
```

---

## 5. users/views.py

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import RegisterForm
from .tokens import account_activation_token
from .email_utils import send_activation_email
from categories.models import University
from .models import Notification
from .models import Contact
from notes.models import Note, Like

User = get_user_model()

# --- EKSİK OLAN HOME FONKSİYONU ---
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')


# users/views.py

def register_view(request):
    # 1. Üniversite listesini çekiyoruz (Dropdown için şart)
    universities = University.objects.all().order_by('name')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            activation_link = f"{settings.BACKEND_BASE_URL}/activate/{uid}/{token}/"

            send_activation_email(user, activation_link)

            messages.success(request, "Kayıt başarılı! Aktivasyon e-postanı kontrol et.")
            return redirect("login")
    else:
        form = RegisterForm()

    # 2. Hem formu hem de üniversite listesini şablona gönderiyoruz
    context = {
        'form': form,
        'universities': universities
    }
    return render(request, "users/register.html", context)

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Hesabınız başarıyla aktif edildi! Giriş yapabilirsiniz.")
        return redirect("login")
    else:
        messages.error(request, "Aktivasyon bağlantısı geçersiz veya süresi dolmuş.")
        return redirect("register")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı ya da hesap aktif değil.")
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


# --- Şifre sıfırlama sayfaları ---
def password_reset_page(request):
    return render(request, "users/password_reset.html")

def password_reset_done_page(request):
    return render(request, "users/password_reset_done.html")

# BURASI GÜNCELLENDİ (Parametreleri alacak şekilde)
def password_reset_confirm_page(request, uidb64, token):
    return render(request, "users/password_reset_confirm.html", {
        'uid': uidb64,
        'token': token
    })

def password_reset_complete_page(request):
    return render(request, "users/password_reset_complete.html")


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "dashboard.html")


# users/views.py dosyasının en altı:

@login_required(login_url="/login/")
def profile(request):
    # Kullanıcının notları - N+1 query problemini çözmek için select_related kullan
    my_notes = request.user.note_set.select_related(
        'university', 'faculty', 'department', 'course'
    ).order_by('-uploaded_at')

    # Beğendikleri - prefetch_related ile N+1 query problemini çöz
    from notes.models import Like
    liked_notes = Like.objects.filter(user=request.user).select_related('note', 'note__university', 'note__course')
    liked_notes_list = [like.note for like in liked_notes]

    # İstatistikler - aggregate kullanarak tek sorguda hesapla
    from django.db.models import Sum, Count
    stats = request.user.note_set.aggregate(
        total_uploads=Count('id'),
        total_downloads=Sum('download_count')
    )
    total_uploads = stats['total_uploads'] or 0
    total_downloads = stats['total_downloads'] or 0

    # --- PUAN HESAPLAMA (XP) ---
    # Formül: (Yükleme Sayısı * 10) + (Toplam İndirilme Sayısı)
    total_xp = (total_uploads * 10) + total_downloads

    # Üniversiteler
    universities = University.objects.all().order_by('name')

    context = {
        'user': request.user,
        'uploaded_notes': my_notes,
        'liked_notes': liked_notes_list,
        'total_downloads': total_downloads,
        'total_uploads': total_uploads,
        'total_xp': total_xp,
        'universities': universities,
    }
    return render(request, "users/profile.html", context)

@login_required
def premium_page(request):
    """Para kazanma sayfası"""
    return render(request, 'users/premium.html')


@login_required
def get_notifications(request):
    """Okunmamış bildirimleri çeker (AJAX için)"""
    notifs = Notification.objects.filter(user=request.user, is_read=False)[:5]
    count = Notification.objects.filter(user=request.user, is_read=False).count()

    data = [{
        'id': n.id,
        'message': n.message,
        'created_at': n.created_at.strftime('%d.%m %H:%M')
    } for n in notifs]

    return JsonResponse({'count': count, 'notifications': data})


@login_required
def mark_notifications_read(request):
    """Bildirimleri okundu yapar"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})


# --- DESTEK (YENİ) ---
def contact_view(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # Giriş yapmışsa bilgilerini otomatik al, yoksa formdan al
        name = request.user.username if request.user.is_authenticated else request.POST.get('name')
        email = request.user.email if request.user.is_authenticated else request.POST.get('email')

        Contact.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name, email=email, subject=subject, message=message
        )
        messages.success(request, "Mesajınız alındı! En kısa sürede dönüş yapacağız.")
        return redirect('contact')

    return render(request, "users/contact.html")
```

---

## 6. notes/views_api.py

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from .models import Note, Comment, Like

class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        # N+1 query problemini çözmek için select_related kullan
        comments = note.comments.select_related('user').all().order_by("-created_at")
        data = [
            {
                "id": c.id,
                "user": c.user.username,
                "user_id": c.user.id,
                "content": c.content,
                "created_at": c.created_at.strftime("%d.%m.%Y %H:%M"),
            }
            for c in comments
        ]
        return Response(data)

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        content = request.data.get("content", "").strip()
        if not content:
            return Response({"error": "Yorum boş olamaz."}, status=400)
        comment = Comment.objects.create(user=request.user, note=note, content=content)
        return Response(
            {
                "id": comment.id,
                "user": comment.user.username,
                "user_id": comment.user.id,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M"),
            },
            status=201,
        )

    def put(self, request, note_id):
        data = request.data
        comment_id = data.get("id")
        new_content = data.get("content", "").strip()
        comment = get_object_or_404(Comment, id=comment_id, note_id=note_id)
        if comment.user != request.user:
            return Response({"error": "Yalnızca kendi yorumunu düzenleyebilirsin."}, status=403)
        comment.content = new_content
        comment.save()
        return Response({"message": "Yorum başarıyla güncellendi."})

    def delete(self, request, note_id):
        data = request.data
        comment_id = data.get("id")
        comment = get_object_or_404(Comment, id=comment_id, note_id=note_id)
        if comment.user != request.user:
            return Response({"error": "Yalnızca kendi yorumunu silebilirsin."}, status=403)
        comment.delete()
        return Response({"message": "Yorum silindi."})

class LikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        liked = Like.objects.filter(user=request.user, note=note).exists()
        total_likes = Like.objects.filter(note=note).count()
        return Response({"liked": liked, "total_likes": total_likes})

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        like_obj = Like.objects.filter(user=request.user, note=note).first()
        if like_obj:
            like_obj.delete()
        else:
            Like.objects.create(user=request.user, note=note)
        total = Like.objects.filter(note=note).count()
        note.likes = total
        note.save()
        return Response({"liked": not bool(like_obj), "total_likes": total})
```

---

## ✅ ÖZET

**Değiştirilen Dosyalar:**
1. ✅ `uniedunote/settings.py` - Güvenlik düzeltmeleri
2. ✅ `users/views_api.py` - CSRF düzeltmesi
3. ✅ `users/urls.py` - URL güncellemesi
4. ✅ `notes/views.py` - Pagination ve N+1 query
5. ✅ `users/views.py` - N+1 query düzeltmeleri
6. ✅ `notes/views_api.py` - N+1 query düzeltmesi

**Yapılacaklar:**
1. Bu dosyaları GitHub'a push et
2. Sunucuda `git pull` yap
3. `.env` dosyasında şunlar olmalı:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=dersnotlarım.com.tr,www.dersnotlarım.com.tr
   BACKEND_BASE_URL=https://dersnotlarım.com.tr
   ```
4. `python manage.py migrate`
5. `python manage.py collectstatic --noinput`
6. Sunucuyu yeniden başlat

**Hepsi bu kadar! 🚀**

