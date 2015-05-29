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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, default='Cube Drone', help_text='The title of your comic')),
                ('tagline', models.CharField(max_length=200, default='Code/comics, updates Tuesday & Thursday', help_text='A short tagline for your comic')),
                ('elevator_pitch', models.TextField(help_text='A Tweet-length description of your comic.', default='Comics about software development in a small Vancouver startup.')),
                ('author_name', models.CharField(max_length=100, default='Curtis Lassam', help_text="What's the author (or author's) names?")),
                ('author_website', models.CharField(max_length=100, default='http://curtis.lassam.net', help_text='Does the author have a personal website?')),
                ('google_tracking_code', models.CharField(max_length=50, default='UA-41279849-1')),
                ('youtube_channel', models.CharField(max_length=150, default='http://www.youtube.com/user/IkoIkoComic/playlists')),
                ('twitter_username', models.CharField(max_length=50, default='classam')),
                ('twitter_widget_id', models.CharField(max_length=50, default='304715092187025408')),
                ('twitter_consumer_key', models.CharField(max_length=100, default='', help_text='Get from apps.twitter.com')),
                ('twitter_consumer_secret', models.CharField(max_length=100, default='', help_text='Get from apps.twitter.com')),
                ('twitter_access_key', models.CharField(max_length=100, default='', help_text='Get from apps.twitter.com')),
                ('twitter_access_secret', models.CharField(max_length=100, default='', help_text='Get from apps.twitter.com')),
            ],
        ),
    ]
