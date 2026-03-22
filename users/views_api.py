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
from uniedunote.rate_limit import check_rate_limit, get_client_ip
from uniedunote.logger_config import get_logger, sanitize_log_data

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger = get_logger('uniedunote')
        
        # Rate limit kontrolü
        is_allowed, error_msg, wait_time = check_rate_limit(request, 'register')
        if not is_allowed:
            logger.warning(f"Rate limit aşıldı (register) - IP: {get_client_ip(request)}")
            return Response({
                'error': error_msg,
                'wait_time': wait_time
            }, status=429)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            activation_link = f"{settings.BACKEND_BASE_URL}/activate/{uid}/{token}/"

            send_activation_email(user, activation_link)
            
            logger.info(f"Yeni kullanıcı kaydı - Kullanıcı: {user.username}, Email: {user.email}, IP: {get_client_ip(request)}")

            return Response({"message": "Kayıt başarılı! Aktivasyon e-postası gönderildi."}, status=201)
        
        logger.warning(f"Geçersiz kayıt denemesi - IP: {get_client_ip(request)}, Hatalar: {sanitize_log_data(serializer.errors)}")
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
        from uniedunote.logger_config import get_logger, sanitize_log_data
        logger = get_logger('uniedunote.security')
        
        # Rate limit kontrolü
        is_allowed, error_msg, wait_time = check_rate_limit(request, 'login')
        if not is_allowed:
            logger.warning(f"Rate limit aşıldı - IP: {get_client_ip(request)}")
            return Response({
                'error': error_msg,
                'wait_time': wait_time
            }, status=429)
        
        try:
            login_input = request.data.get("username")  # Bu email de olabilir, username de
            password = request.data.get("password")

            if not login_input or not password:
                logger.warning(f"Eksik giriş bilgisi - IP: {get_client_ip(request)}")
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
                logger.info(f"Başarılı giriş - Kullanıcı: {user.username}, IP: {get_client_ip(request)}")
                return Response({"message": "Login başarılı", "username": user.username})
            else:
                logger.warning(f"Başarısız giriş denemesi - Kullanıcı: {login_input}, IP: {get_client_ip(request)}")
                return Response({"error": "Giriş bilgileri hatalı!"}, status=401)

        except Exception as e:
            logger.error(f"Giriş hatası - IP: {get_client_ip(request)}, Hata: {str(e)}", exc_info=True)
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
            except Exception:
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