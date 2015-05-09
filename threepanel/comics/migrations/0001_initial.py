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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100, help_text='The title of the blog post')),
                ('markdown', models.TextField(help_text='The blog content')),
                ('markdown_rendered', models.TextField(blank=True, help_text='The blog content, rendered into HTML', default='')),
                ('hidden', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100, help_text='The title of the comic', unique_for_date='posted')),
                ('posted', models.DateTimeField(db_index=True, help_text='The date the comic should be published')),
                ('image_url', models.CharField(max_length=300, help_text="The url to the comic's image file")),
                ('secret_text', models.TextField(blank=True, help_text='A small amount of text that pops up below the comic', default='')),
                ('alt_text', models.TextField(blank=True, help_text='A complete transcript of the text, for screenreaders\n                    and search engines', default='')),
                ('promo_text', models.CharField(blank=True, max_length=80, help_text='A less-than-80 character promo/teaser for the comic, posted with\n                     the comic on Twitter/RSS/what-have-you', default='')),
                ('order', models.PositiveIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('tags', taggit.managers.TaggableManager(verbose_name='Tags', help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='comic',
            field=models.ForeignKey(related_name='blogs', to='comics.Comic'),
        ),
    ]
