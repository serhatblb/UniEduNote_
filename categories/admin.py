from django.contrib import admin
from .models import University, Faculty, Department, Course
admin.site.register([University, Faculty, Department, Course])
