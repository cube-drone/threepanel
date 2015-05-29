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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(help_text='The title of your comic', default='Cube Drone', max_length=100)),
                ('tagline', models.CharField(help_text='A short tagline for your comic', default='Code/comics, updates Tuesday & Thursday', max_length=200)),
                ('elevator_pitch', models.TextField(help_text='A Tweet-length description of your comic.', default='Comics about software development in a small Vancouver startup.')),
                ('author_name', models.CharField(help_text="What's the author (or author's) names?", default='Curtis Lassam', max_length=100)),
                ('author_website', models.CharField(help_text='Does the author have a personal website?', default='http://curtis.lassam.net', max_length=100)),
                ('google_tracking_code', models.CharField(default='UA-41279849-1', max_length=50)),
                ('twitter_username', models.CharField(default='classam', max_length=50)),
                ('twitter_widget_id', models.CharField(default='304715092187025408', max_length=50)),
                ('twitter_consumer_key', models.CharField(help_text='Get from apps.twitter.com', default='', max_length=100)),
                ('twitter_consumer_secret', models.CharField(help_text='Get from apps.twitter.com', default='', max_length=100)),
                ('twitter_access_key', models.CharField(help_text='Get from apps.twitter.com', default='', max_length=100)),
                ('twitter_access_secret', models.CharField(help_text='Get from apps.twitter.com', default='', max_length=100)),
            ],
        ),
    ]
