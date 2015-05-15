from django.db import models
from django.contrib.auth.models import User


class Memo(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(default=" ")
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', null=True)
    chosen = models.BooleanField(default=False)
    owner = models.ForeignKey(User)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
