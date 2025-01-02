from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    last_updated = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=6, null=True, blank=True) 
    otp_expiry = models.DateTimeField(null=True, blank=True)
