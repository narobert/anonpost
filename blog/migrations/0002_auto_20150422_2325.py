# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcomment',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 23, 25, 41, 720217)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppost',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 23, 25, 41, 714738)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wcomment',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 23, 25, 41, 717732)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wpost',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 23, 25, 41, 712249)),
            preserve_default=True,
        ),
    ]
