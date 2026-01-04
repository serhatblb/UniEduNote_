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