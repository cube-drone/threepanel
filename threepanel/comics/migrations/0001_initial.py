# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.UUIDField(serialize=False, editable=False, primary_key=True, default=uuid.uuid4)),
                ('title', models.CharField(unique_for_date='posted', max_length=100)),
                ('posted', models.DateTimeField(db_index=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('image_url', models.CharField(max_length=300)),
                ('secret_text', models.TextField(default='', blank=True)),
                ('alt_text', models.TextField(default='', blank=True)),
                ('hidden', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
        ),
    ]
