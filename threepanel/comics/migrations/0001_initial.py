# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import djorm_fulltext.fields
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='The title of the blog post')),
                ('markdown', models.TextField(help_text='The blog content')),
                ('markdown_rendered', models.TextField(blank=True, help_text='The blog content, rendered into HTML', default='')),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique=True)),
                ('title', models.CharField(max_length=100, help_text='The title of the comic', unique_for_date='posted')),
                ('posted', models.DateTimeField(db_index=True, help_text='The date the comic should be published')),
                ('image_url', models.CharField(max_length=300, help_text="The url to the comic's image file")),
                ('secret_text', models.TextField(blank=True, help_text='A small amount of text that pops up below the comic', default='')),
                ('alt_text', models.TextField(blank=True, help_text='A complete transcript of the text, for screenreaders\n                    and search engines', default='')),
                ('promo_text', models.CharField(blank=True, max_length=80, default='', help_text='A less-than-80 character promo/teaser for the comic, posted with\n                     the comic on Twitter/RSS/what-have-you')),
                ('order', models.PositiveIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('tags', django.contrib.postgres.fields.ArrayField(blank=True, size=None, base_field=models.CharField(max_length=50), null=True)),
                ('search_index', djorm_fulltext.fields.VectorField()),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='The title of the image')),
                ('image_url', models.CharField(max_length=300, help_text='The url to the image file')),
                ('secret_text', models.TextField(blank=True, help_text='A small amount of text that pops up below the image', default='')),
                ('alt_text', models.TextField(blank=True, help_text='A complete transcript of the image, for screenreaders\n                    and search engines', default='')),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique=True)),
                ('comic', models.ForeignKey(to='comics.Comic', related_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='The title of the video')),
                ('youtube_video_code', models.CharField(max_length=20, help_text="The youtube video code - like 'izGwDsrQ1eQ'")),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique=True)),
                ('comic', models.ForeignKey(to='comics.Comic', related_name='video')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='comic',
            field=models.ForeignKey(to='comics.Comic', related_name='blogs'),
        ),
    ]
