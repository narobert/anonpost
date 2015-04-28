# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150422_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcomment',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 23, 25, 57, 304689)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppost',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 23, 25, 57, 299230)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wcomment',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 23, 25, 57, 302213)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wpost',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 23, 25, 57, 296700)),
            preserve_default=True,
        ),
    ]
