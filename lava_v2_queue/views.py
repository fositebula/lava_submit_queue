# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import traceback

from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
from models import VerifyData, VerifyDataTmp
from form import VerifyDataForm, VerifyDataTmpForm, RunningLogTmpForm
from django.core.exceptions import ObjectDoesNotExist
import json
# Create your views here.

# lava_submit/push/?buildlist=1&build_id=1&submit_user=1&verify_url=1&gerrit_id=1&port=1&
# compile_user=1&module=1&
# test_cases=1&manual_test_case=1&phone_number=1&test_description=1&project_num=1&test_task_type=1
def push(request):
    if request.method == "GET":
        try:
            vf = VerifyDataForm(request.GET)
            if vf.is_valid():
                vf.save()
                return HttpResponse('ok')
        except Exception as e:
            return HttpResponse(e.message)
def pop(request):
    if request.method == "GET":
        try:
            verify_data = VerifyData.objects.filter(submitted_flag=0)
            if  len(verify_data) == 0:
                return HttpResponse("No data for submitting!")
            vdd = verify_data.values(
                "id",
                "buildlist",
                "build_id",
                "submit_user",
                "verify_url",
                "gerrit_id",
                "port",
                "compile_user",
                "module",
                "test_cases",
                "manual_test_case",
                "phone_number",
                "test_description",
                "project_num",
                "test_task_type",
            )[0]
            j_str = json.dumps(vdd)
            return HttpResponse(j_str)
        except Exception as e:
            return HttpResponse(e.message)

def push_tmp(request):
    print request.GET
    if request.method == "GET":
        try:
            vf = VerifyDataTmpForm(request.GET)
            # if vf.is_valid():
            vf.save()
            return HttpResponse('ok')
        except Exception as e:
            return HttpResponse(e.message)
    return HttpResponse("Push Fail!")
#http://10.0.70.33:8000/lava_submit/push/?buildlist=1&build_id=1&submit_user=1&verify_url=1&gerrit_id=1&port=1&compile_user=1&module=1&test_cases=1&manual_test_case=1&phone_number=1&test_description=1&project_num=1&test_task_type=1
def pop_tmp(request):
    if request.method == "GET":
        try:
            verify_data = VerifyDataTmp.objects.filter(submitted_flag=0)
            if  len(verify_data) == 0:
                return HttpResponse("No data for submitting!")
            vdd = verify_data.values(
                "id",
                "branch",
                "project",
                "build_id",
                "submit_user",
                "verify_url",
                "gerrit_id",
                "port",
                "compile_user",
                "module",
                "test_cases",
                "manual_test_case",
                "phone_number",
                "test_description",
                "project_num",
                "test_task_type",
            )[0]
            j_str = json.dumps(vdd)
            return HttpResponse(j_str)
        except Exception as e:
            return HttpResponse(e.message)

def update_tmp(request):
    if request.method == "POST":
        m_id = request.POST.get("id")
        jobid = request.POST.get("lavaJobid")
        running_log = request.FILES.get("log")
        print running_log.read()
        try:
            info = VerifyDataTmp.objects.get(id=m_id)
        except ObjectDoesNotExist:
            return HttpResponse('Not found by id.')
        if jobid:
            info.lavaJobId =jobid
        if running_log:
            info.submitted_flag = 1
            info.submitting_log = running_log
            info.save()
            return HttpResponse('ok')
    return HttpResponse(dict(request.POST))

def upload_files(request):
    if request.method == "POST":
            #print request.FILES
            id = request.POST["id"]
            verify_data = VerifyDataTmp.objects.get(id=id)
            f = request.FILES["log"]
            print f
            verify_data.submitting_log = f
            verify_data.save()
            return HttpResponse("upload successfully!")


def index(request):
    return HttpResponse("Welcome!!!")