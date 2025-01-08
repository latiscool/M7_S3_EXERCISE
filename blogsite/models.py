from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)


class Meta:
    ordering = ["-created_on"]


def __str__(self):
    return self.title


def save(self, *args, **kargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kargs)


def get_absolute_url(self):
    return reverse("blog_post_detail", args=[self.slug])


""" 

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)
    
"""
