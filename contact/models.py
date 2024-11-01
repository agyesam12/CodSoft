from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=False, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=GENDER, default="other")
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username