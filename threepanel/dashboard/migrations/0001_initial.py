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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(help_text='The title of your comic', max_length=100, default='Cube Drone')),
                ('tagline', models.CharField(help_text='A short tagline for your comic', max_length=200, default='Code/comics, updates Tuesday & Thursday')),
                ('elevator_pitch', models.TextField(help_text='A Tweet-length description of your comic.', default='Comics about software development in a small Vancouver startup.')),
                ('author_name', models.CharField(help_text="What's the author (or author's) names?", max_length=100, default='Curtis Lassam')),
                ('author_website', models.CharField(help_text='Does the author have a personal website?', max_length=100, default='http://curtis.lassam.net')),
                ('google_tracking_code', models.CharField(default='UA-41279849-1', max_length=50)),
                ('youtube_channel', models.CharField(default='http://www.youtube.com/user/IkoIkoComic/playlists', max_length=150)),
                ('twitter_username', models.CharField(default='classam', max_length=50)),
                ('twitter_widget_id', models.CharField(default='304715092187025408', max_length=50)),
                ('twitter_consumer_key', models.CharField(help_text='Get from apps.twitter.com', max_length=100, default='')),
                ('twitter_consumer_secret', models.CharField(help_text='Get from apps.twitter.com', max_length=100, default='')),
                ('twitter_access_key', models.CharField(help_text='Get from apps.twitter.com', max_length=100, default='')),
                ('twitter_access_secret', models.CharField(help_text='Get from apps.twitter.com', max_length=100, default='')),
            ],
        ),
    ]
