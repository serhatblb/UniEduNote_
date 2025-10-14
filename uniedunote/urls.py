from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect

from users.views import register_view, login_view, logout_view, activate_account
from notes.views import upload_note, note_list, note_detail, download_note


def home(request):
    """Giriş yapmamış kullanıcılar için ana sayfa (landing page)"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'base.html')


def dashboard(request):
    """Giriş yapan kullanıcılar için ana panel"""
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')


def profile(request):
    """Kullanıcı profil sayfası"""
    if not request.user.is_authenticated:
        return redirect('login')

    uploaded_notes = request.user.note_set.all()
    total_downloads = sum(note.download_count for note in uploaded_notes)
    return render(request, 'profile.html', {
        'user': request.user,
        'uploaded_notes': uploaded_notes,
        'total_downloads': total_downloads
    })


urlpatterns = [
    path('admin/', admin.site.urls),

    # Web sayfaları
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),

    # Kullanıcı işlemleri
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),

    # Notlar
    path('upload/', upload_note, name='upload_note'),
    path('notes/', note_list, name='note_list'),
    path('notes/<int:pk>/', note_detail, name='note_detail'),
    path('notes/<int:pk>/download/', download_note, name='download_note'),

    # API’ler
    path('api/auth/', include('users.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
