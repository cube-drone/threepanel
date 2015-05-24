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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100, help_text='The title of the blog post')),
                ('markdown', models.TextField(help_text='The blog content')),
                ('markdown_rendered', models.TextField(default='', blank=True, help_text='The blog content, rendered into HTML')),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('search_index', djorm_fulltext.fields.VectorField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('title', models.CharField(help_text='The title of the comic', max_length=100, unique_for_date='posted')),
                ('posted', models.DateTimeField(db_index=True, help_text='The date the comic should be published')),
                ('image_url', models.CharField(max_length=300, help_text="The url to the comic's image file")),
                ('secret_text', models.TextField(default='', blank=True, help_text='A small amount of text that pops up below the comic')),
                ('alt_text', models.TextField(default='', blank=True, help_text='A complete transcript of the text, for screenreaders\n                    and search engines')),
                ('promo_text', models.CharField(default='', max_length=80, help_text='A less-than-80 character promo/teaser for the comic, posted with\n                     the comic on Twitter/RSS/what-have-you', blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None, blank=True, null=True)),
                ('search_index', djorm_fulltext.fields.VectorField()),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='comic',
            field=models.ForeignKey(to='comics.Comic', related_name='blogs'),
        ),
    ]
