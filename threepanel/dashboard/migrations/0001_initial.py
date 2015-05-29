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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(default='Cube Drone', help_text='The title of your comic', max_length=100)),
                ('tagline', models.CharField(default='Code/comics, updates Tuesday & Thursday', help_text='A short tagline for your comic', max_length=200)),
                ('elevator_pitch', models.TextField(default='Comics about software development in a small Vancouver startup.', help_text='A Tweet-length description of your comic.')),
                ('author_name', models.CharField(default='Curtis Lassam', help_text="What's the author (or author's) names?", max_length=100)),
                ('author_website', models.CharField(default='http://curtis.lassam.net', help_text='Does the author have a personal website?', max_length=100)),
                ('google_tracking_code', models.CharField(default='UA-41279849-1', max_length=50)),
                ('youtube_channel', models.CharField(default='http://www.youtube.com/user/IkoIkoComic', max_length=150)),
                ('twitter_username', models.CharField(default='classam', max_length=50)),
                ('twitter_widget_id', models.CharField(default='304715092187025408', max_length=50)),
                ('twitter_consumer_key', models.CharField(default='', help_text='Get from apps.twitter.com', max_length=100)),
                ('twitter_consumer_secret', models.CharField(default='', help_text='Get from apps.twitter.com', max_length=100)),
                ('twitter_access_key', models.CharField(default='', help_text='Get from apps.twitter.com', max_length=100)),
                ('twitter_access_secret', models.CharField(default='', help_text='Get from apps.twitter.com', max_length=100)),
            ],
        ),
    ]
