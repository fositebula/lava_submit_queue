# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Blog
from models import VerifyData

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from lava.models import User

# Register your models here.
class BlogModelAdmin(admin.ModelAdmin):
    pass

class VerifyDataAdmin(admin.ModelAdmin):
    list_display = ('build_id', 'branch', 'project', 'submit_user')

admin.site.register(Blog, BlogModelAdmin)
admin.site.register(VerifyData, VerifyDataAdmin)