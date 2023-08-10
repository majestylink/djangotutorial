import time

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from account.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.FileField(upload_to='recipes/', blank=True, null=True)
    slug = models.SlugField(default='', blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self):
        # self.uploaded_date = timezone.now()
        base_slug = slugify(self.title)
        timestamp = int(time.time())
        unique_slug = f"{base_slug}-{timestamp}"
        self.slug = unique_slug
        super(Recipe, self).save()

    def get_absolute_url(self):
        return reverse('recipe:detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    moderation = models.BooleanField(default=True)

    def __str__(self):
        return self.text
