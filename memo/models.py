from django.db import models
from django.contrib.auth.models import User


class Memo(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(default=" ")
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', null=True, blank=True)
    chosen = models.BooleanField(default=False)
    owner = models.ForeignKey(User)
    published = models.BooleanField(default=False)

    def as_dict(self):
        category = ''
        if self.category:
            category = self.category.name

        d = dict(
            pk=self.pk,
            title=self.title,
            text=self.text,
            created=self.created.isoformat(),
            category=category,
            chosen=self.chosen,
            published=self.published,
            owner=self.owner.username
        )
        return d

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
