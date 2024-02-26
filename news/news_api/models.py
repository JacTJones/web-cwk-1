from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Test(models.Model):
    name = models.CharField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Story(models.Model):
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=6)
    region = models.CharField(max_length=2)
    details = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    story_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.headline
