from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ("Link", "link"),
    ("Note", "note"),
    ("Memo", "memo"),
    ("ToDo", "todo"),
]


class Memo(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(default=" ")
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    chosen = models.BooleanField(default=False)
    owner = models.ForeignKey(User)