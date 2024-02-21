# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=150, null=True)  # Add address field

    def __str__(self):
        return self.user.username
