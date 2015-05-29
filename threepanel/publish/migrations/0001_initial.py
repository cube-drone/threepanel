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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('email', models.CharField(unique=True, max_length=100)),
                ('verification_code', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('last_email_sent', models.DateTimeField()),
            ],
        ),
    ]
