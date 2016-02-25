# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-20 05:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_siteoptions_slug'),
        ('publish', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailsubscriber',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='email_subscribers', to='dashboard.SiteOptions'),
        ),
    ]