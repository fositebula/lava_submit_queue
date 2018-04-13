# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import User

class VerifyData(models.Model):
    branch = models.CharField(max_length=50)
    project = models.CharField(max_length=50)
    build_id = models.CharField(max_length=50)
    submit_user = models.CharField(max_length=50)
    verify_url = models.CharField(max_length=50)
    gerrit_id = models.CharField(max_length=50)
    port = models.CharField(max_length=50)
    compile_user = models.CharField(max_length=50)
    module = models.CharField(max_length=50)
    test_cases = models.CharField(max_length=50)
    manual_test_case = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    test_description = models.CharField(max_length=50)
    project_num = models.CharField(max_length=50)
    test_task_type = models.CharField(max_length=50)
    submit_time = models.IntegerField(default=0)

class Blog(models.Model):
    title = models.CharField(max_length=100)
    artcle = models.TextField(max_length=1000)
    publice_time = models.DateTimeField(auto_now=True)
    author_name = models.CharField(max_length=50)
    shorthand = models.CharField(max_length=50)

    # @models.permalink
    def url(self):
        return reverse(viewname="blog_detail", kwargs={"blogid":self.pk})

class School(models.Model):
    name = models.CharField(max_length=100)
    addr = models.CharField(max_length=100)

class Person(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=20)
    school = models.ForeignKey(School)