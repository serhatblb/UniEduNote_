from django.contrib import admin
from .models import Note, Comment, Like, Bookmark, Report


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'university', 'course', 'download_count', 'likes', 'uploaded_at')
    list_filter = ('university', 'uploaded_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('uploaded_at', 'download_count', 'likes')
    date_hierarchy = 'uploaded_at'
    ordering = ('-uploaded_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content', 'note__title')
    readonly_fields = ('created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'note__title')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'created_at')
    search_fields = ('user__username', 'note__title')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'note', 'reason', 'is_resolved', 'created_at')
    list_filter = ('reason', 'is_resolved')
    search_fields = ('reporter__username', 'note__title')
    actions = ['mark_resolved']

    @admin.action(description='Seçili raporları çözümlendi olarak işaretle')
    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
