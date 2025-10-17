from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from uniedunote import settings
from .tokens import account_activation_token
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()


# ✅ Kullanıcı Kaydı
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            current_site = get_current_site(request)
            subject = "UniEduNote Hesap Aktivasyonu"
            message = render_to_string("users/activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return Response({"message": "Kayıt başarılı! Aktivasyon e-postası gönderildi."}, status=201)
        return Response(serializer.errors, status=400)


# ✅ Hesap Aktivasyonu
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
            return Response({"error": "Bu e-posta adresi kayıtlı değil."}, status=400)

        current_site = get_current_site(request)
        subject = "UniEduNote Şifre Sıfırlama"
        message = render_to_string("users/password_reset_email.html", {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        return Response({"message": "Şifre sıfırlama e-postası gönderildi."})


# ✅ Şifre sıfırlama (doğrulama)
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


# ✅ JWT + Session entegrasyonu
@csrf_exempt
def session_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"error": "JSON bekleniyor"}, status=400)

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Kullanıcı adı ve şifre zorunlu"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return JsonResponse({"message": "Login başarılı", "username": user.username})
        else:
            return JsonResponse({"error": "Geçersiz kullanıcı adı veya şifre"}, status=401)

    return JsonResponse({"error": "Yalnızca POST isteği destekleniyor"}, status=405)

# ✅ Profil Güncelleme (JWT zorunlu)
class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        university = data.get("university", "").strip()
        password = data.get("password", "").strip()

        # E-posta veya kullanıcı adı boş olamaz
        if not username or not email:
            return Response({"error": "Kullanıcı adı ve e-posta zorunludur."}, status=400)

        # Mevcut şifreyle aynı olmasın (şimdilik basit kontrol)
        if password and user.check_password(password):
            return Response({"error": "Yeni şifre eskiyle aynı olamaz."}, status=400)

        user.username = username
        user.email = email
        if email != user.email:
            return Response({"error": "E-posta değişikliği e-posta doğrulaması gerektirir."}, status=400)

        # Üniversite alanı backend modelinde varsa kaydet
        if hasattr(user, "university") and university:
            user.university = university

        # Şifre değişikliği istenmişse uygula
        if password:
            user.set_password(password)

        user.save()
        return Response({"message": "Profil başarıyla güncellendi."})
