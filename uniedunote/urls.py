# uniedunote/urls.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
import traceback
# --- YENİ EKLEME (Scripti çağırmak için) ---
from django.http import HttpResponse
import db_setup  # Senin db_setup dosyanı çağırıyoruz


def kurtarici_setup(request):
    try:
        messages = []
        User = get_user_model()

        # 1. Veritabanı Bağlantısını Test Et
        # Eğer bağlantı yoksa burada patlar
        user_count = User.objects.count()
        messages.append(f"📡 Veritabanı bağlantısı başarılı! Mevcut kullanıcı sayısı: {user_count}")

        # 2. Admin Hesabı Kontrolü
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
            messages.append("✅ Admin hesabı oluşturuldu! (admin / admin1234)")
        else:
            messages.append("ℹ️ Admin hesabı zaten var.")

        # 3. Üniversiteleri Yükle
        import db_setup
        db_setup.run()
        messages.append("✅ Üniversiteler başarıyla yüklendi.")

        return HttpResponse("<br>".join(messages))

    except Exception as e:
        # HATAYI EKRANA BASAN KISIM
        error_details = traceback.format_exc()
        return HttpResponse(f"""
            <h1>💥 BİR HATA OLDU KANKA!</h1>
            <p>Hata Mesajı: {str(e)}</p>
            <hr>
            <h3>Teknik Detay (Bunu bana at):</h3>
            <pre>{error_details}</pre>
        """, status=500)


# ---------------------------------------------

# Diğer view importların...
from notes.views import upload_note, note_list, note_detail, download_note, edit_note, delete_note
from users.views import (
    register_view, login_view, logout_view, activate_account,
    password_reset_page, password_reset_done_page,
    password_reset_confirm_page, password_reset_complete_page
)
from notes import views as note_views  # AJAX için


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'base.html')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')


def profile(request):
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

    # --- GİZLİ KURULUM LİNKİ ---
    path('kurtar-bizi-baba/', kurtarici_setup),
    # ---------------------------

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
    path('notes/<int:pk>/edit/', edit_note, name='edit_note'),
    path('notes/<int:pk>/delete/', delete_note, name='delete_note'),

    # AJAX (Dropdown doldurma)
    path('ajax/load-faculties/', note_views.load_faculties, name='ajax_load_faculties'),
    path('ajax/load-departments/', note_views.load_departments, name='ajax_load_departments'),
    path('ajax/load-courses/', note_views.load_courses, name='ajax_load_courses'),

    # API’ler
    path('api/auth/', include('users.urls')),
    path("api/notes/", include("notes.urls")),

    # Şifre sıfırlama
    path("password-reset/", password_reset_page, name="password_reset"),
    path("password-reset/done/", password_reset_done_page, name="password_reset_done"),
    path("password-reset/confirm/", password_reset_confirm_page, name="password_reset_confirm"),
    path("password-reset/complete/", password_reset_complete_page, name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)