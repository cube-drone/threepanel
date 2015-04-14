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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Super Cool Comic X', max_length=100, help_text='The title of your comic')),
                ('tagline', models.CharField(default='A super cool comic about things!', max_length=100, help_text='A short tagline for your comic')),
                ('elevator_pitch', models.TextField(default='', help_text='A Tweet-length description of your comic.')),
                ('mobile_logo_url', models.CharField(default='http://butts.butts/butts.jpg', max_length=200, help_text='The URL for the mobile-sized (width:300px, height:150px) logo to the website.')),
                ('desktop_logo_url', models.CharField(default='http://butts.butts/deskbutts.jpg', max_length=200, help_text='The URL for the desktop-sized (width:500px, height:100px) logo to the website.')),
            ],
        ),
    ]
