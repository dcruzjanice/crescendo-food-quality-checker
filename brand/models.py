from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=250, null=True)
    district = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=6, null=True)
    state = models.CharField(max_length=100, null=True)
    fssai_no = models.CharField(max_length=14, null=True)
    is_approved = models.BooleanField(default=False, null=True)
    auth_token = models.CharField(max_length=100, null=True)
    is_verified = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    year = models.IntegerField(null=True)  
    is_validated = models.BooleanField(default=False, null=True) 
    last_inspected_date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.username if self.user else ""
