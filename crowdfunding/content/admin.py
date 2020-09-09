from django.contrib import admin
from .models import Project, Pledge, Category, ImageLibrary

# Register your models here.
admin.site.register(Project)
admin.site.register(Pledge)
admin.site.register(Category)
admin.site.register(ImageLibrary)