# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-13 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lava_v2_queue', '0003_verifydatatmp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifydatatmp',
            name='submitting_log',
            field=models.FileField(null=True, upload_to='logs/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='verifydatatmp',
            name='verify_url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
