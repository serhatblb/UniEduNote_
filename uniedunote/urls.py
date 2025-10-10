from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from users.views import register_view, login_view, logout_view
from notes.views import upload_note, note_list, note_detail, download_note
from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def profile(request):
    return render(request, 'profile.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Ana sayfa doğrudan dashboard
    path('', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),

    # Kullanıcı
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # Notlar
    path('upload/', upload_note, name='upload_note'),
    path('notes/', note_list, name='note_list'),
    path('notes/<int:pk>/', note_detail, name='note_detail'),
    path('notes/<int:pk>/download/', download_note, name='download_note'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def profile(request):
    user = request.user
    uploaded_notes = user.note_set.all()
    total_downloads = sum(note.download_count for note in uploaded_notes)
    context = {
        'user': user,
        'uploaded_notes': uploaded_notes,
        'total_downloads': total_downloads
    }
    return render(request, 'profile.html', context)
