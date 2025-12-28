from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- 1. AKADEMİK MODELLER ---
class University(models.Model):
    name = models.CharField(max_length=200, verbose_name="Üniversite Adı")
    logo = models.ImageField(upload_to='uni_logos/', blank=True, null=True)

    def __str__(self): return self.name

class Faculty(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="faculties")
    name = models.CharField(max_length=200)

    def __str__(self): return f"{self.university.name} - {self.name}"

class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=200)

    def __str__(self): return f"{self.faculty.name} - {self.name}"

class Course(models.Model):
    CLASS_YEAR_CHOICES = [(1, '1. Sınıf'), (2, '2. Sınıf'), (3, '3. Sınıf'), (4, '4. Sınıf'), (5, 'Hazırlık/Diğer')]
    TERM_SEASON_CHOICES = [('Guz', 'Güz Dönemi'), ('Bahar', 'Bahar Dönemi'), ('Yaz', 'Yaz Okulu')]

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True)
    class_year = models.IntegerField(choices=CLASS_YEAR_CHOICES, default=1)
    term_season = models.CharField(max_length=10, choices=TERM_SEASON_CHOICES, default='Guz')

    def __str__(self): return f"{self.code} - {self.name}"

class Note(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='notes/')
    created_at = models.DateTimeField(auto_now_add=True)
    downloads = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=True)

    def __str__(self): return self.title

# --- 2. KULLANICI PROFİL SİSTEMİ (YENİ) ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Hakkımda")
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)
    points = models.IntegerField(default=10, verbose_name="Puan") # Kayıt bonusu 10 puan

    def __str__(self): return f"{self.user.username} Profili"

# Kullanıcı oluşunca otomatik Profil de oluştur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()