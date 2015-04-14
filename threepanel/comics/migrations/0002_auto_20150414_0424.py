# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='alt_text',
            field=models.TextField(default='', blank=True, help_text='A complete transcript of the text, for screenreaders\n                    and search engines'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='image_url',
            field=models.CharField(help_text="The url to the comic's image file", max_length=300),
        ),
        migrations.AlterField(
            model_name='comic',
            name='posted',
            field=models.DateTimeField(help_text='The date the comic should be published', db_index=True),
        ),
        migrations.AlterField(
            model_name='comic',
            name='secret_text',
            field=models.TextField(default='', blank=True, help_text='A small amount of text that pops up below the comic'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='title',
            field=models.CharField(help_text='The title of the comic', max_length=100, unique_for_date='posted'),
        ),
    ]
