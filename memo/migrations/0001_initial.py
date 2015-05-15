# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(default=' ')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('Link', 'link'), ('Note', 'note'), ('Memo', 'memo'), ('ToDo', 'todo')], max_length=200)),
                ('chosen', models.BooleanField(default=False)),
            ],
        ),
    ]
