# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteOptions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100, default='Cube Drone', help_text='The title of your comic')),
                ('tagline', models.CharField(max_length=100, default='Code/comics, updates Tuesday & Thursday', help_text='A short tagline for your comic')),
                ('elevator_pitch', models.TextField(default='Comics about software development in a small Vancouver startup.', help_text='A Tweet-length description of your comic.')),
                ('email', models.CharField(max_length=100, default='curtis@lassam.net', help_text='The site sends e-mail from this address.')),
                ('author_name', models.CharField(max_length=100, default='Curtis Lassam', help_text="What's the author (or author's) names?")),
                ('author_website', models.CharField(max_length=100, default='http://curtis.lassam.net', help_text='Does the author have a personal website?')),
                ('google_tracking_code', models.CharField(max_length=50, default='UA-41279849-1')),
                ('twitter_username', models.CharField(max_length=50, default='classam')),
                ('twitter_widget_id', models.CharField(max_length=50, default='304715092187025408')),
            ],
        ),
    ]
