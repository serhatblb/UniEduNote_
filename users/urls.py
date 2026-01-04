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
