from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from notes import views as note_views
from chat import views as chat_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Web Sayfaları ---
    path('', user_views.home, name='home'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('profile/', user_views.profile, name='profile'),

    # --- Kullanıcı İşlemleri ---
    path('login/', user_views.login_view, name='login'),
    path('register/', user_views.register_view, name='register'),
    path('logout/', user_views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', user_views.activate_account, name='activate'),

    # --- Şifre Sıfırlama ---
    path("password-reset/", user_views.password_reset_page, name="password_reset"),
    path("password-reset/done/", user_views.password_reset_done_page, name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', user_views.password_reset_confirm_page, name='password_reset_confirm'),
    path("password-reset/complete/", user_views.password_reset_complete_page, name="password_reset_complete"),

    # --- Notlar ---
    path('upload/', note_views.upload_note, name='upload_note'),
    path('notes/', note_views.note_list, name='note_list'),
    path('notes/<int:pk>/', note_views.note_detail, name='note_detail'),
    path('notes/<int:pk>/download/', note_views.download_note, name='download_note'),
    path('notes/<int:pk>/edit/', note_views.edit_note, name='edit_note'),
    path('notes/<int:pk>/delete/', note_views.delete_note, name='delete_note'),

    # --- AJAX ---
    path('ajax/load-faculties/', note_views.load_faculties, name='ajax_load_faculties'),
    path('ajax/load-departments/', note_views.load_departments, name='ajax_load_departments'),
    path('ajax/load-courses/', note_views.load_courses, name='ajax_load_courses'),

    # --- API ---
    path('api/auth/', include('users.urls')),
    path("api/notes/", include("notes.urls")),

    path('chat/', chat_views.chat_room, name='chat_room'),
    path('chat/get/', chat_views.get_messages, name='get_messages'),
    path('chat/send/', chat_views.send_message, name='send_message'),

    # Premium
    path('premium/', user_views.premium_page, name='premium'),

    path('contact/', user_views.contact_view, name='contact'),

    # Bildirimler
    path('api/notifications/get/', user_views.get_notifications, name='get_notifications'),
    path('api/notifications/read/', user_views.mark_notifications_read, name='mark_notifications_read'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)