# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ppost',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'#', primary_key=True)),
                ('date', models.DateField(default=datetime.datetime(2015, 4, 14, 4, 59, 38, 194906))),
                ('profilepost', models.CharField(max_length=1000)),
                ('clicked', models.BooleanField(default=False)),
                ('user1', models.ForeignKey(related_name='user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(related_name='user2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wpost',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'#', primary_key=True)),
                ('date', models.DateField(default=datetime.datetime(2015, 4, 14, 4, 59, 38, 191744))),
                ('wallpost', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
