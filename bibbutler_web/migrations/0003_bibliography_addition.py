# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibbutler_web', '0002_auto_20160601_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliography',
            name='addition',
            field=models.CharField(blank=True, help_text='additional infos like version or something', max_length=20),
        ),
    ]