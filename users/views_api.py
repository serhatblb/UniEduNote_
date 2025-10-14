from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterSerializer, MyTokenObtainPairSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from .tokens import account_activation_token

User = get_user_model()

class RegisterAPIView(APIView):
    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        domain = get_current_site(request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = f"http://{domain}/api/auth/activate/{uid}/{token}/"
        subject = "UniEduNote hesap aktivasyonu"
        message = f"Merhaba {user.username},\nHesabını aktifleştir: {activation_link}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response({"detail":"Kayıt alındı. Aktivasyon maili gönderildi."}, status=201)

class ActivateAPIView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"detail":"Geçersiz bağlantı."}, status=400)
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"detail":"Hesap aktifleştirildi."}, status=200)
        return Response({"detail":"Token geçersiz veya süresi dolmuş."}, status=400)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        ser = PasswordResetRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Bilgi sızdırmamak için her durumda success döneriz.
            return Response({"detail":"Eğer kayıtlıysanız mail gönderdik."}, status=200)
        domain = get_current_site(request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)  # PasswordResetTokenGenerator ile aynı mantık
        link = f"http://{domain}/reset-password/confirm?uidb64={uid}&token={token}"
        send_mail("Şifre sıfırlama", f"Bağlantı: {link}", settings.DEFAULT_FROM_EMAIL, [email])
        return Response({"detail":"Eğer kayıtlıysanız mail gönderdik."}, status=200)

class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        ser = PasswordResetConfirmSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        uidb64 = ser.validated_data['uidb64']
        token = ser.validated_data['token']
        new_pw = ser.validated_data['new_password']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"detail":"Geçersiz bağlantı."}, status=400)
        if account_activation_token.check_token(user, token):
            user.set_password(new_pw)
            user.save()
            return Response({"detail":"Şifre güncellendi."}, status=200)
        return Response({"detail":"Token geçersiz veya süresi dolmuş."}, status=400)
