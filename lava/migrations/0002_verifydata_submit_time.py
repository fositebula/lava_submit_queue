# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-26 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lava', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifydata',
            name='submit_time',
            field=models.IntegerField(default=0),
        ),
    ]
