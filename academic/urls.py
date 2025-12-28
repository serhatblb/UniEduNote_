from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),

    # Akademik Linkler
    path('department/<int:department_id>/', views.department_detail, name='department_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/upload/', views.upload_note, name='upload_note'),
    
    # Email Activation
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]