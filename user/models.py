from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles',)
    profilepic = models.ImageField(upload_to='images/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    
    #def get_age(self):
        