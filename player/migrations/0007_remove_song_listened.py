# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-12 19:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_auto_20160810_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='listened',
        ),
    ]
