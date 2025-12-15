from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    # Admin panelinde görünecek sütunlar
    list_display = ['username', 'email', 'university', 'rank', 'is_staff']

    # Hangi alanlara göre link verileceği
    list_display_links = ['username', 'email']

    # Düzenleme sayfasındaki alanlar (fieldsets)
    fieldsets = UserAdmin.fieldsets + (
        ('Ekstra Bilgiler', {'fields': ('university', 'avatar')}),
    )

    # Yeni kullanıcı ekleme sayfasındaki alanlar
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Ekstra Bilgiler', {'fields': ('university', 'avatar')}),
    )


admin.site.register(User, CustomUserAdmin)