# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import djorm_fulltext.fields
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='The title of the blog post')),
                ('markdown', models.TextField(help_text='The blog content')),
                ('markdown_rendered', models.TextField(help_text='The blog content, rendered into HTML', blank=True, default='')),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('title', models.CharField(unique_for_date='posted', max_length=100, help_text='The title of the comic')),
                ('posted', models.DateTimeField(help_text='The date the comic should be published', db_index=True)),
                ('image_url', models.CharField(max_length=300, help_text="The url to the comic's image file")),
                ('secret_text', models.TextField(help_text='A small amount of text that pops up below the comic', blank=True, default='')),
                ('alt_text', models.TextField(help_text='A complete transcript of the text, for screenreaders\n                    and search engines', blank=True, default='')),
                ('promo_text', models.CharField(max_length=80, help_text='A less-than-80 character promo/teaser for the comic, posted with\n                     the comic on Twitter/RSS/what-have-you', blank=True, default='')),
                ('order', models.PositiveIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('tags', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=50), null=True, blank=True)),
                ('search_index', djorm_fulltext.fields.VectorField()),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='The title of the image')),
                ('image_url', models.CharField(max_length=300, help_text='The url to the image file')),
                ('secret_text', models.TextField(help_text='A small amount of text that pops up below the image', blank=True, default='')),
                ('alt_text', models.TextField(help_text='A complete transcript of the image, for screenreaders\n                    and search engines', blank=True, default='')),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('comic', models.ForeignKey(related_name='image', to='comics.Comic')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='The title of the video')),
                ('youtube_video_code', models.CharField(max_length=20, help_text="The youtube video code - like 'izGwDsrQ1eQ'")),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('comic', models.ForeignKey(related_name='video', to='comics.Comic')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='comic',
            field=models.ForeignKey(related_name='blogs', to='comics.Comic'),
        ),
    ]
