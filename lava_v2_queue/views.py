# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import traceback

from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render

from lava_v2_queue.tables import VerifyTables
from models import VerifyData, VerifyDataTmp
from form import VerifyDataForm, VerifyDataTmpForm, RunningLogTmpForm
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import json
# Create your views here.
import logging
logger = logging.getLogger("django") # 为loggers中定义的名称
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
            print e
            return HttpResponse(e.message)
    return HttpResponse("Push Fail!")
#http://10.0.70.33:8000/lava_submit/push/?buildlist=1&build_id=1&submit_user=1&verify_url=1&gerrit_id=1&port=1&compile_user=1&module=1&test_cases=1&manual_test_case=1&phone_number=1&test_description=1&project_num=1&test_task_type=1
def pop_tmp(request):
    if request.method == "GET":
        try:
            verify_data = VerifyDataTmp.objects.filter(submitted_flag=0).filter(poped_flag=0)
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
            v = VerifyDataTmp.objects.get(id=vdd["id"])
            v.poped_flag = 1
            v.save()
            j_str = json.dumps(vdd)
            print "poptmp", j_str
            logger.info(j_str)
            return HttpResponse(j_str)
        except Exception as e:
            return HttpResponse(e.message)

def update_tmp(request):
    if request.method == "POST":
        m_id = request.POST.get("id")
        jobid = request.POST.get("lavaJobid")
        running_log = request.FILES.get("log")
        logstr = running_log.read()

        find_job = re.findall("jobid:\((\d*)\)", logstr, re.S)
        if len(find_job) != 0:
            jobid = find_job[0]
            print "JobID: ", jobid
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

def get_lava_jobs(request):
    if request.method == 'GET':
        jobs = []
        jobs_q = VerifyDataTmp.objects.exclude(lavaJobId='')
        for job in jobs_q:
            jobs.append(job.lavaJobId)

        return HttpResponse(", ".join(jobs))

def get_data_infos(request):
    if request.method == "GET":
        table = VerifyTables(VerifyDataTmp.objects.exclude(lavaJobId=''))
        return render(request, 'VerifyDataInfo.html', {'table':table})

def get_log(request, year, month, day, file_name):
    logger.info( "/".join([year, month, day, file_name]))
    # return HttpResponse("/".join([year, month, day, file_name]))
    file_path = '{media_path}/logs/{year}/{month}/{day}/{file}'.format(media_path=settings.MEDIA_URL, year=year, month=month, day=day, file=file_name)
    file_name = file_name
    if request.method == "GET":
        if not os.path.exists(file_path):
            return HttpResponse('No file: %s'%file_path)
        with open(file_path, 'rb') as fd:
            log_str = fd.read()
            log_str = log_str.replace('\n', '<br \>')
            log_str = "<h3> %s </h3>"%file_name + log_str
            return HttpResponse(log_str)

def index(request):
    return HttpResponse("Welcome!!!")