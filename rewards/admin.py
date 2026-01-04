from django.contrib import admin
from .models import UserProfile, PointTransaction, Badge


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'total_xp', 'total_notes_created', 'total_likes_received', 'total_downloads_received', 'daily_login_streak')
    list_filter = ('level', 'profile_completed')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('total_xp', 'level', 'created_at', 'updated_at')
    ordering = ('-total_xp',)


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'points', 'note', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge_type', 'earned_at')
    list_filter = ('badge_type', 'earned_at')
    search_fields = ('user__username',)
    readonly_fields = ('earned_at',)
    ordering = ('-earned_at',)
