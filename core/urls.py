from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Bunu import et
from academic import views as academic_views # Kayıt view'ı için
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('academic.urls')),

    # GİRİŞ - ÇIKIŞ
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', academic_views.signup, name='signup'),  # Bunu aşağıda yazacağız
]

# Medya dosyaları (Resim, PDF) için ayar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)