# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150422_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcomment',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 23, 8, 30, 56, 162566)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppost',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 23, 8, 30, 56, 157115)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wcomment',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 23, 8, 30, 56, 160078)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wpost',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 23, 8, 30, 56, 154537)),
            preserve_default=True,
        ),
    ]
