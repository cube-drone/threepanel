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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(help_text='The title of your comic', max_length=100, default='Cube Drone')),
                ('tagline', models.CharField(help_text='A short tagline for your comic', max_length=100, default='Code/comics, updates Tuesday & Thursday')),
                ('elevator_pitch', models.TextField(help_text='A Tweet-length description of your comic.', default='Comics about software development in a small Vancouver startup.')),
                ('email', models.CharField(help_text='The site sends e-mail from this address.', max_length=100, default='curtis@lassam.net')),
                ('author_name', models.CharField(help_text="What's the author (or author's) names?", max_length=100, default='Curtis Lassam')),
                ('author_website', models.CharField(help_text='Does the author have a personal website?', max_length=100, default='http://curtis.lassam.net')),
                ('google_tracking_code', models.CharField(max_length=50, default='UA-41279849-1')),
                ('twitter_username', models.CharField(max_length=50, default='classam')),
                ('twitter_widget_id', models.CharField(max_length=50, default='304715092187025408')),
            ],
        ),
    ]
