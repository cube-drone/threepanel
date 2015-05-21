# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSubscriber',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('verification_code', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('last_email_sent', models.DateTimeField()),
            ],
        ),
    ]
