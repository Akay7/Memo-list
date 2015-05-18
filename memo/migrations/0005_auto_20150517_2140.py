# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0004_auto_20150515_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='memo',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='memo',
            name='category',
            field=models.ForeignKey(to='memo.Category', blank=True, null=True),
        ),
    ]
