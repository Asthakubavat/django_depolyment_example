from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    profile_pic = models.ImageField(upload_to='profile_pic',blank=True)

    portfolio = models.URLField(blank=True)

# Create your models here.
