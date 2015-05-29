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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='The title of your comic', default='Cube Drone')),
                ('tagline', models.CharField(max_length=200, help_text='A short tagline for your comic', default='Code/comics, updates Tuesday & Thursday')),
                ('elevator_pitch', models.TextField(help_text='A Tweet-length description of your comic.', default='Comics about software development in a small Vancouver startup.')),
                ('author_name', models.CharField(max_length=100, help_text="What's the author (or author's) names?", default='Curtis Lassam')),
                ('author_website', models.CharField(max_length=100, help_text='Does the author have a personal website?', default='http://curtis.lassam.net')),
                ('google_tracking_code', models.CharField(max_length=50, default='UA-41279849-1')),
                ('youtube_channel', models.CharField(max_length=150, default='http://www.youtube.com/user/IkoIkoComic/playlists')),
                ('patreon_page', models.CharField(max_length=150, default='https://www.patreon.com/cubedrone')),
                ('twitter_username', models.CharField(max_length=50, default='classam')),
                ('twitter_widget_id', models.CharField(max_length=50, default='304715092187025408')),
                ('twitter_consumer_key', models.CharField(max_length=100, help_text='Get from apps.twitter.com', default='')),
                ('twitter_consumer_secret', models.CharField(max_length=100, help_text='Get from apps.twitter.com', default='')),
                ('twitter_access_key', models.CharField(max_length=100, help_text='Get from apps.twitter.com', default='')),
                ('twitter_access_secret', models.CharField(max_length=100, help_text='Get from apps.twitter.com', default='')),
            ],
        ),
    ]
