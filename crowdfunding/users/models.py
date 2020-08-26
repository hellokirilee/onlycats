from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    pass
    def __str__(self):
        return self.username
