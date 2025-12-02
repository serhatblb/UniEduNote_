from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .tokens import account_activation_token
from .email_utils import send_activation_email

User = get_user_model()


def register_view(request):
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
    return render(request, "users/register.html", {"form": form})


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


# Şifre sıfırlama sayfaları (şimdilik sadece template render)
def password_reset_page(request):
    return render(request, "users/password_reset.html")


def password_reset_done_page(request):
    return render(request, "users/password_reset_done.html")


def password_reset_confirm_page(request):
    return render(request, "users/password_reset_confirm.html")


def password_reset_complete_page(request):
    return render(request, "users/password_reset_complete.html")


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "dashboard.html")


@login_required(login_url="/login/")
def profile(request):
    return render(request, "profile.html")


@login_required(login_url="/login/")
def upload_note(request):
    return render(request, "upload_note.html")


@login_required(login_url="/login/")
def note_list(request):
    return render(request, "note_list.html")
