from typing import cast
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import render
from users.models import UserProfile


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True, primary_key=True)
    def __str__(self):
        return self.category


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length = 200)
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField()
    date_released = models.DateTimeField(null=True)
    owner = models.ForeignKey(
        "users.UserProfile",
        on_delete=models.CASCADE,
        related_name='owner_projects',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null = True
    )

class ImageLibrary(models.Model):
    content_img_name = models.CharField(max_length=200)
    content_img = models.URLField(max_length = 200, verbose_name = 'Content Image URL')
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='images'
    )


class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        #change delete to not cascade later
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )
