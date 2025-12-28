from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Contact, Notification


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'university', 'rank', 'is_staff']
    list_display_links = ['username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Ekstra Bilgiler', {'fields': ('university', 'avatar', 'is_premium')}),
    )

    # Yeni kullanıcı ekleme sayfasındaki alanlar
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Ekstra Bilgiler', {'fields': ('university', 'avatar')}),
    )

# Contact Admin (YENİ)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'created_at', 'is_resolved']
    list_filter = ['is_resolved', 'subject']
    search_fields = ['message', 'email']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Notification)