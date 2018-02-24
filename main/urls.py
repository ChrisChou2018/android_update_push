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
from django.conf.urls import url, include
from . import views, views_api

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index.do$',                                              views.index,            name = 'index'),                  # 首页：我的App
    url(r'^add_app.do$',                                            views.add_app,          name = 'add_app'),                # 首页：添加App
    url(r'^(?P<appid>[0-9]+)/patch_issued.do$',                     views.patch_issued,     name = 'patch_issued'),           # 补丁下发
    url(r'^(?P<appid>[0-9]+)/add_app_version.do$',                  views.add_app_version,  name = "add_app_version"),        # 添加app版本
    url(r'^(?P<appid>[0-9]+)/(?P<id>[0-9]+)/add_patch.do$',         views.add_patch,        name = "add_patch"),              # 发布补丁
    url(r'^(?P<appid>[0-9]+)/(?P<id>[0-9]+)/patch_details.do$',     views.patch_details,    name = "patch_details"),          # 补丁下发详情
    url(r'^(?P<appid>[0-9]+)/online_datas.do$',                     views.online_datas,     name = "online_datas"),           # 在线参数
    url(r'^(?P<appid>[0-9]+)/monitor.do$',                          views.monitor,          name = "monitor"),                # 实时监控
    url(r'^(?P<appid>[0-9]+)/histroy.do$',                          views.histroy,          name = "histroy"),                # 历史补丁
    url(r'^(?P<appid>[0-9]+)/(?P<id>[0-9]+)/histroy_details.do',    views.histroy_details,  name = "histroy_details"),        # 历史补丁详情
    url(r'^(?P<appid>[0-9]+)/app_information.do$',                  views.app_information,  name = "app_information"),        # app信息
]

urlpatterns += [
    url(r'^api/add_app.do$',                views_api.add_app),                         # 添加App
    url(r'^api/add_online_datas.do$',       views_api.add_online_datas),                # 新增在线参数
    url(r'^api/delete_online_datas.do$',    views_api.delete_online_datas),             # 删除在线参数
    url(r'^api/add_app_version.do$',        views_api.add_app_version),                 # 添加app版本号
    url(r'^api/delete_patch.do$',           views_api.delete_patch),                    # 删除下发补丁
    url(r'^api/update_patch.do$',           views_api.update_patch),                    # 恢复、暂停补丁下发
    url(r'^api/get_patch_version$',         views_api.get_patch_version),               
    url(r'api/get_chart_data$',             views_api.get_chart_data),
]
