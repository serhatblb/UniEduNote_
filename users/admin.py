from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'university', 'points', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'university')
    list_filter = ('is_active', 'is_staff')

