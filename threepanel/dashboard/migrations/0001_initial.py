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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(default='Cube Drone', max_length=100, help_text='The title of your comic')),
                ('tagline', models.CharField(default='Code/comics, updates Tuesday & Thursday', max_length=100, help_text='A short tagline for your comic')),
                ('elevator_pitch', models.TextField(default='Comics about software development in a small Vancouver startup.', help_text='A Tweet-length description of your comic.')),
                ('email', models.CharField(default='curtis@lassam.net', max_length=100, help_text='The site sends e-mail from this address.')),
                ('author_name', models.CharField(default='Curtis Lassam', max_length=100, help_text="What's the author (or author's) names?")),
                ('author_website', models.CharField(default='http://curtis.lassam.net', max_length=100, help_text='Does the author have a personal website?')),
                ('google_tracking_code', models.CharField(default='UA-41279849-1', max_length=50)),
                ('twitter_username', models.CharField(default='classam', max_length=50)),
                ('twitter_widget_id', models.CharField(default='304715092187025408', max_length=50)),
            ],
        ),
    ]
