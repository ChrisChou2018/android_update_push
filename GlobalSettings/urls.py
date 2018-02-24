# -*- coding: utf-8 -*-

"""GlobalSettings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from main import views_api

urlpatterns = [
    url(r'^main/',              include('main.urls')),              # 入口
]

urlpatterns += [
    url(r'^api/v1/patch$',                   views_api.has_new_patch),                # 检查是否有新的补丁
    url(r'^api/v1/success$',                  views_api.return_code),
    url(r'^api/v1/fail$',                     views_api.return_code),
    url(r'^api/v1/pvlog$',                       views_api.pv_log),
]

# @TODO(phw):
# 为了在使用runserver命令起服务时能photologue等能正常获取media/下的内容，
# 在linux上线时可以关闭，因为在正式部署时，media目录是通过apache控制的
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

