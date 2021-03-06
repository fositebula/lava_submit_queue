# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-11 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lava_v2_queue', '0002_verifydata_submitted_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyDataTmp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(default='', max_length=50)),
                ('branch', models.CharField(default='', max_length=50)),
                ('build_id', models.CharField(default='', max_length=50)),
                ('submit_user', models.CharField(default='', max_length=50)),
                ('verify_url', models.CharField(default='', max_length=50)),
                ('gerrit_id', models.CharField(default='', max_length=50)),
                ('port', models.CharField(default='', max_length=50)),
                ('compile_user', models.CharField(default='', max_length=50)),
                ('module', models.CharField(default='', max_length=50)),
                ('test_cases', models.CharField(default='', max_length=50)),
                ('manual_test_case', models.CharField(default='', max_length=50)),
                ('phone_number', models.CharField(default='', max_length=50)),
                ('test_description', models.CharField(default='', max_length=50)),
                ('project_num', models.CharField(default='', max_length=50)),
                ('test_task_type', models.CharField(default='', max_length=50)),
                ('submitted_flag', models.IntegerField(default=0)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('lavaJobId', models.CharField(default='', max_length=10)),
                ('submitting_log', models.FileField(upload_to='logs/%Y/%m/%d')),
            ],
        ),
    ]
