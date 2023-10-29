from django.db import models
from django.contrib.auth import get_user

from cloudinary.models import CloudinaryField

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default='Uncategorized')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField("image", blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    pass
