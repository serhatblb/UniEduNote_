from django.contrib import admin
from .models import University, Faculty, Department, Course, Note

# Dersleri panelde güzel listelemek için ayar
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'class_year', 'term_season')
    list_filter = ('department', 'class_year', 'term_season')

# Notları panelde güzel listelemek için ayar
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploader', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')

# Şimdi hepsini kaydediyoruz
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Course, CourseAdmin)
admin.site.register(Note, NoteAdmin)