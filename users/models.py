from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    university = models.ForeignKey('categories.University', null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name='users')
    points = models.IntegerField(default=0)
    stars = models.IntegerField(default=1)
