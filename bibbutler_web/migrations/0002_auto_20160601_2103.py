# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 21:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibbutler_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': 'Generic entry', 'verbose_name_plural': 'Generic entries'},
        ),
        migrations.AlterModelOptions(
            name='entrybook',
            options={'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
        migrations.AlterModelOptions(
            name='entryonline',
            options={'verbose_name': 'Online', 'verbose_name_plural': 'Online entrys'},
        ),
    ]