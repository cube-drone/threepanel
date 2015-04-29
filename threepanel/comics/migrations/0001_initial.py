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
            name='Comic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(unique_for_date='posted', max_length=100, help_text='The title of the comic')),
                ('posted', models.DateTimeField(db_index=True, help_text='The date the comic should be published')),
                ('image_url', models.CharField(max_length=300, help_text="The url to the comic's image file")),
                ('secret_text', models.TextField(default='', blank=True, help_text='A small amount of text that pops up below the comic')),
                ('alt_text', models.TextField(default='', blank=True, help_text='A complete transcript of the text, for screenreaders\n                    and search engines')),
                ('order', models.PositiveIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
        ),
    ]
