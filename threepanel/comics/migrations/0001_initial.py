# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(help_text='The title of the blog post', max_length=100)),
                ('markdown', models.TextField(help_text='The blog content')),
                ('markdown_rendered', models.TextField(default='', help_text='The blog content, rendered into HTML', blank=True)),
                ('hidden', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(unique_for_date='posted', max_length=100, help_text='The title of the comic')),
                ('posted', models.DateTimeField(help_text='The date the comic should be published', db_index=True)),
                ('image_url', models.CharField(help_text="The url to the comic's image file", max_length=300)),
                ('secret_text', models.TextField(default='', help_text='A small amount of text that pops up below the comic', blank=True)),
                ('alt_text', models.TextField(default='', help_text='A complete transcript of the text, for screenreaders\n                    and search engines', blank=True)),
                ('promo_text', models.CharField(default='', max_length=80, help_text='A less-than-80 character promo/teaser for the comic, posted with\n                     the comic on Twitter/RSS/what-have-you', blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='comic',
            field=models.ForeignKey(to='comics.Comic', related_name='blogs'),
        ),
    ]
