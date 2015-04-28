# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150423_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcomment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 23, 20, 22, 46, 670776)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppost',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 23, 20, 22, 46, 665332)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wcomment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 23, 20, 22, 46, 668307)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wpost',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 23, 20, 22, 46, 662823)),
            preserve_default=True,
        ),
    ]
