# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(help_text='The title of the blog post', max_length=100)),
                ('markdown', models.TextField(help_text='The blog content')),
                ('markdown_rendered', models.TextField(blank=True, help_text='The blog content, rendered into HTML', default='')),
                ('hidden', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('title', models.CharField(help_text='The title of the comic', max_length=100, unique_for_date='posted')),
                ('posted', models.DateTimeField(help_text='The date the comic should be published', db_index=True)),
                ('image_url', models.CharField(help_text="The url to the comic's image file", max_length=300)),
                ('secret_text', models.TextField(blank=True, help_text='A small amount of text that pops up below the comic', default='')),
                ('alt_text', models.TextField(blank=True, help_text='A complete transcript of the text, for screenreaders\n                    and search engines', default='')),
                ('promo_text', models.CharField(blank=True, help_text='A less-than-80 character promo/teaser for the comic, posted with\n                     the comic on Twitter/RSS/what-have-you', max_length=80, default='')),
                ('order', models.PositiveIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('tags', django.contrib.postgres.fields.ArrayField(blank=True, size=None, base_field=models.CharField(max_length=50), null=True)),
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
