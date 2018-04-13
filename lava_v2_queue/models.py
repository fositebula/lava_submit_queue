# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class VerifyData(models.Model):
    buildlist = models.CharField(max_length=1000, default="")
    build_id = models.CharField(max_length=50, default="")
    submit_user = models.CharField(max_length=50, default="")
    verify_url = models.CharField(max_length=50, default="")
    gerrit_id = models.CharField(max_length=50, default="")
    port = models.CharField(max_length=50, default="")
    compile_user = models.CharField(max_length=50, default="")
    module = models.CharField(max_length=50, default="")
    test_cases = models.CharField(max_length=50, default="")
    manual_test_case = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=50, default="")
    test_description = models.CharField(max_length=50, default="")
    project_num = models.CharField(max_length=50, default="")
    test_task_type = models.CharField(max_length=50, default="")
    submitted_flag = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now=True)

class VerifyDataTmp(models.Model):
    project = models.CharField(max_length=50, default="")
    branch = models.CharField(max_length=50, default="")
    build_id = models.CharField(max_length=50, default="")
    submit_user = models.CharField(max_length=50, default="")
    verify_url = models.CharField(max_length=200, default="")
    gerrit_id = models.CharField(max_length=50, default="")
    port = models.CharField(max_length=50, default="")
    compile_user = models.CharField(max_length=50, default="")
    module = models.CharField(max_length=50, default="")
    test_cases = models.CharField(max_length=50, default="")
    manual_test_case = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=50, default="")
    test_description = models.CharField(max_length=50, default="")
    project_num = models.CharField(max_length=50, default="")
    test_task_type = models.CharField(max_length=50, default="")

    date_time = models.DateTimeField(auto_now=True)

    submitted_flag = models.IntegerField(default=0)
    lavaJobId = models.CharField(max_length=10, default="")
    submitting_log = models.FileField(upload_to='logs/%Y/%m/%d', null=True)