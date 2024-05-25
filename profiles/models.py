# profiles/models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('ONG', 'ONG'),
        ('Voluntier', 'Voluntier'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True)

    def __str__(self):
        return self.user.username
