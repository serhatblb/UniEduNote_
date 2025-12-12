from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    university = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
