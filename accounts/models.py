from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):

    ROLE_CHOICES = (
        ('USER', 'User'),
        ('DOCTOR', 'Doctor'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='USER'
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    registration_number = models.CharField(max_length=50, blank=True, null=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username