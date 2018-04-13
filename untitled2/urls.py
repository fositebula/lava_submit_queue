"""untitled2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import urls, views
from lava import views as lava_view
from lava_v2_queue import views as queue_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^search/$', lava_view.search),
    url(r'^insert/$', lava_view.insertVerifyData),
    url(r'^get/$', lava_view.get),
    url(r'^index/$', lava_view.index),
    url(r'^rebuild/$', lava_view.rebuild),
    url(r'^register/$', lava_view.register_view, name='register'),
    url(r'^login/$', lava_view.login_view, name='login'),
    url(r'^blogs/$', lava_view.blog_list, name='blogs'),
    url(r'^blog_detail/$', lava_view.blog_detail, name='blog_detail'),
    url(r'^lava_submit/$', queue_view.index, name='queue_index'),
    url(r'^lava_submit/push/$', queue_view.push, name='queue_push'),
    url(r'^lava_submit/pop/$', queue_view.pop, name='queue_pop'),
    url(r'^lava_submit/pushtmp/$', queue_view.push_tmp, name='queue_push_tmp'),
    url(r'^lava_submit/poptmp/$', queue_view.pop_tmp, name='queue_pop_tmp'),
    url(r'^lava_submit/updatetmp/$', queue_view.update_tmp, name='queue_update_tmp'),
]
