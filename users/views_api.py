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
from django.views.decorators.csrf import csrf_exempt
from .email_utils import send_activation_email

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
            # Güvenlik için kullanıcı yoksa bile "Gönderildi" diyelim (User Enumeration engellemek için)
            # Ama test aşamasında hata dönebiliriz. Şimdilik hata dönelim:
            return Response({"error": "Bu e-posta adresi kayıtlı değil."}, status=400)

        # Token ve UID oluştur
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        # Linki settings'den alalım (Daha güvenli)
        reset_link = f"{settings.BACKEND_BASE_URL}/password-reset-confirm/{uid}/{token}/"

        subject = "UniEduNote Şifre Sıfırlama"
        message = f"Merhaba {user.username},\n\nŞifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:\n\n{reset_link}\n\nEğer bu isteği siz yapmadıysanız dikkate almayın."

        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
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


# ✅ Session login (opsiyonel)
@csrf_exempt
def session_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
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