"""
Akademik hiyerarşi API URL'leri
"""
from django.urls import path
from .views_api import (
    UniversityListView,
    FacultyListView,
    DepartmentListView,
    CourseListView,
    CourseGetOrCreateView,
    AcademicSearchView
)

urlpatterns = [
    path('universities/', UniversityListView.as_view(), name='api-universities'),
    path('faculties/', FacultyListView.as_view(), name='api-faculties'),
    path('departments/', DepartmentListView.as_view(), name='api-departments'),
    path('courses/', CourseListView.as_view(), name='api-courses'),
    path('courses/create/', CourseGetOrCreateView.as_view(), name='api-courses-create'),
    path('search/', AcademicSearchView.as_view(), name='api-academic-search'),
]

