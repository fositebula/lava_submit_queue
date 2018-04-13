# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_tables2 import RequestConfig
from pymongo import MongoClient
import json

from lava.blogs_table import BlogTable
from lava.resubmit import get_query_data, get_json_data

from lava.resubmit import resubmit
from models import VerifyData, Blog
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from .form import UserForm
from bs4 import BeautifulSoup


# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    buildid = request.GET['buildid']
    client = MongoClient('10.0.70.68', 27017)
    db = client['LAVA']
    tb = db['gerrit_do_verify_sprdroid8.x_91']
    docs = tb.find({'buildid':buildid}, {"_id":0})
    client.close()
    j_data = json.dumps(list(docs))
    print docs.count()
    return HttpResponse(j_data)
#?branch=sprdroid8.1_trunk_18b&project=s9863a1h10_nosec-userdebug-native&build_id=49588&submit_user=mingmin.ling&verify_url=http://cmverify.spreadtrum.com:8080/jenkins/job/gerrit_do_verify_sprdroid8.x/49588/&gerrit_id='466664,1'&port=29418&compile_user=mingmin.ling&module=poweron&test_cases='default'&manual_test_case='{poweron[adbcheck,poweron]}'&phone_number=1&test_description=latest&project_num=1&test_task_type=verify
def insertVerifyData(request):
    branch = request.GET.get('branch')
    project = request.GET.get('project')
    build_id = request.GET.get('build_id')
    submit_user = request.GET.get('submit_user')
    verify_url = request.GET.get('verify_url')
    gerrit_id = request.GET.get('gerrit_id')
    port = request.GET.get('port')
    compile_user = request.GET.get('compile_user')
    module = request.GET.get('module')
    test_cases = request.GET.get('test_cases')
    manual_test_case = request.GET.get('manual_test_case')
    phone_number = request.GET.get('phone_number')
    test_description = request.GET.get('test_description')
    project_num = request.GET.get('project_num')
    test_task_type = request.GET.get('test_task_type')

    print branch, project, build_id, submit_user, verify_url, gerrit_id, port, \
        compile_user, module, test_cases, manual_test_case, phone_number, test_description, \
        project_num, test_task_type

    vd = VerifyData(branch=branch, project=project, build_id=build_id, submit_user=submit_user, verify_url=verify_url,
                    gerrit_id=gerrit_id, port=port, compile_user=compile_user, module=module, test_cases=test_cases,
                    manual_test_case=manual_test_case, phone_number=phone_number, test_description=test_description,
                    project_num=project_num, test_task_type=test_task_type)
    vd.save()
    return HttpResponse('ok')

def get_build_list(querys):
    datas = querys.values("branch", "project")
    return ",".join(map(lambda info:info["branch"]+":"+info["project"], [info for info in datas]))

def get(request):
    buildid = request.GET.get('buildid')
    datas = VerifyData.objects.filter(build_id=buildid)
    list_str = get_build_list(datas)
    return HttpResponse(list_str)

def get_buildid(html):
    soup = BeautifulSoup(html)
    trs = soup.find_all('tr', 'build-pending')
    if len(trs) == 0:
        trs = soup.find_all('tr', ["build-row", "multi-line", "overflow-checked"])
    for div in trs[0].div:
        if div.string != None:
            return div.string
    return "not found"

#get_query_data(up_build_id, up_jobname, up_verifier, up_change_url, up_module, build_list, testpara
# , test_case, imgnum, monkey_device_amount, stable, upstream_type, monkeytime)
def rebuild(request):
    buildid = request.GET.get('buildid')
    datas = VerifyData.objects.filter(build_id=buildid)
    if len(datas) == 0:
        return HttpResponse("Not Found %s info."%buildid)
    build_list = get_build_list(datas)
    up_build_id = datas[0].build_id + "_"+"".join(random.sample("rebuild", 5))
    up_jobname = datas[0].verify_url.strip().split("/")[-3]
    up_verifier = datas[0].compile_user
    up_change_url = datas[0].gerrit_id
    up_module = datas[0].module
    testpara = datas[0].manual_test_case.strip('\'')
    test_case = datas[0].test_cases
    imgnum = len(datas)
    monkey_device_amount = datas[0].phone_number
    stable = "latest"
    upstream_type = datas[0].test_task_type
    monkeytime = "not"
    j_d = get_json_data(up_build_id, up_jobname, up_verifier, up_change_url, up_module, build_list, testpara,\
				  test_case, imgnum, stable, monkeytime,  monkey_device_amount, upstream_type)
    d_s = get_query_data(up_build_id, up_jobname, up_verifier, up_change_url, up_module, build_list, testpara
    , test_case, imgnum, monkey_device_amount, stable, upstream_type, monkeytime, j_d)
    re =  resubmit(d_s)
    if re.status_code == 200:
        return HttpResponse(get_buildid(re.content))



@csrf_exempt
def register_view(request):
    context = {}
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            print username, password
            print user
            if user:
                context['userExist'] = True
                return render(request, 'register.html', context)
            user = User.objects.create_user(username=username, password=password)
            user.save()

            request.session['username'] = username
            auth.login(request, user)
            return redirect('/index')
    else:
        context['isLogin'] = False
    return render(request, 'register.html', context)

@csrf_exempt
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            print username, password
            print user
            if user:
                auth.login(request, user)
                request.session['username'] = username
                return redirect('/index')
            else:
                context = {'isLogin':False, 'pawd':False}
                return render(request, 'login.html', context)
    else:
        context = {'isLogin': False, 'pawd': False}
    return render(request, 'login.html', context)


def blog_list(request):
    table = BlogTable(Blog.objects.all())
    # table = BlogTable([{'name':'adb', 'storage':'/home/local/SPREADTRUM/pl.dong/adb'}])
    return render(request, 'blog_list.html', {'table':table})

    # context = {}
    # if request.method == "GET":
    #     blogs = Blog.objects.all()
    #     if blogs:
    #         rep = render(request, 'blog_list.html', context={"blogs":blogs})
    #         return rep
    #     else:
    #         return HttpResponse('No blog!')

def blog_detail(request):
    if request.method == "GET":
        blogid = request.GET['blogid']
        blog = Blog.objects.get(id=blogid)
        return render(request, 'blog.html', context={'blog':blog})
    return HttpResponse('Not fond blog!')
