# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-10 18:54
from __future__ import unicode_literals

import autoslug.fields
import dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20160308_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteoptions',
            name='author_name',
            field=models.CharField(help_text="What's the author (or author's) names?", max_length=100),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='author_website',
            field=models.CharField(help_text='Does the author have a personal website?', max_length=100),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='domain',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='elevator_pitch',
            field=models.TextField(help_text='A Tweet-length description of your comic.'),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='google_tracking_code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='patreon_page',
            field=models.CharField(help_text='Link to your Patreon page', max_length=150),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=models.CharField(help_text='The title of your comic', max_length=100), slugify=dashboard.models.slugify, unique=True),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='tagline',
            field=models.CharField(help_text='A short tagline for your comic', max_length=200),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='title',
            field=models.CharField(help_text='The title of your comic', max_length=100),
        ),
        migrations.AlterField(
            model_name='siteoptions',
            name='youtube_channel',
            field=models.CharField(help_text='Link to your YouTube channel', max_length=150),
        ),
    ]
