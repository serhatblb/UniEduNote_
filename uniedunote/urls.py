from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from users.views import login_view, register_view, logout_view  # mevcut server-render sayfalar
from users.views_api import (
    RegisterAPIView, ActivateAPIView,
    MyTokenObtainPairView,
    PasswordResetRequestAPIView, PasswordResetConfirmAPIView
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from notes.views import upload_note, note_list, note_detail, download_note

def home(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return render(request, 'base.html')

def profile(request):
    user = request.user
    uploaded_notes = getattr(user, 'note_set', []).all() if user.is_authenticated else []
    total_downloads = sum(n.download_count for n in uploaded_notes) if user.is_authenticated else 0
    return render(request, 'profile.html', {'user': user,'uploaded_notes': uploaded_notes,'total_downloads': total_downloads})

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web sayfaları
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),

    path('upload/', upload_note, name='upload_note'),
    path('notes/', note_list, name='note_list'),
    path('notes/<int:pk>/', note_detail, name='note_detail'),
    path('notes/<int:pk>/download/', download_note, name='download_note'),

    # Auth API (JWT + Aktivasyon + Şifre Sıfırlama)
    path('api/auth/register/', RegisterAPIView.as_view()),
    path('api/auth/activate/<uidb64>/<token>/', ActivateAPIView.as_view(), name='activate'),
    path('api/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/password/reset/', PasswordResetRequestAPIView.as_view()),
    path('api/auth/password/reset/confirm/', PasswordResetConfirmAPIView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
