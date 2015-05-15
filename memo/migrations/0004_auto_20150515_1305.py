# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0003_auto_20150515_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memo',
            name='category',
            field=models.ForeignKey(to='memo.Category', null=True),
        ),
    ]
