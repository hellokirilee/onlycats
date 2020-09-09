from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    pass
    def __str__(self):
        return self.username

class UserProfile(models.Model):  
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_image_url = models.URLField(max_length = 200, verbose_name = 'Profile Image URL')
    user_bio = models.TextField(max_length = 100, verbose_name = 'Catent Creator Bio')
    

    def __str__(self):
        return u'Profile of user: %s' % self.user.username
