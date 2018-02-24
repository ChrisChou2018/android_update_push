# -*- coding: utf-8 -*-
import urllib, datetime, time, os
import json
from main.hasPushUpdate import has_push_update
from django import forms
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.conf import settings
from django.db.models import Max, Count
from common.Define import RETURN_CODE
from .models import(Online_parameters,
                    Patch,
                    Histroy,
                    AppPack,
                    PatchMonitoring,
                    PV_LOG)


def add_app(request):
    """
    添加App
    """
    if request.method == 'POST' and request.POST:
        appname = request.POST.get('appname')
        packname = request.POST.get('packname')
        if not appname or not packname:
            return JsonResponse({"return_code": RETURN_CODE.FAIL, "return_msg": "app名称和包名都不可为空"})
        exist_appname = AppPack.objects.filter(appname=appname).exists()                  # 验证app名称的唯一性
        if exist_appname:
            return JsonResponse({"return_code": RETURN_CODE.FAIL, "return_msg": "app名称已存在"})
        exist_packname = AppPack.objects.filter(packname=packname).exists()               # 验证包名的唯一性
        if exist_packname:
            return JsonResponse({"return_code": RETURN_CODE.FAIL, "return_msg": "包名已存在"})
        a = AppPack()
        a.appname = appname
        a.packname = packname
        a.save()
        return JsonResponse({"return_code": RETURN_CODE.SUCCESS, "return_msg": "添加App成功"})
    else:
        pass


def add_online_datas(request):
    """
    新增在线参数
    """
    if request.method == 'POST' and request.POST:
        pname = request.POST.get("pname")
        pvalues = request.POST.get("pvalues")
        if not pname:
            return JsonResponse({"return_code":RETURN_CODE.FAIL, "return_msg":"参数名称不能为空"})
        if not pvalues:
            return JsonResponse({"return_code":RETURN_CODE.FAIL, "return_msg":"参数值不能为空"})
        params = {"pname":pname, "pvalues":pvalues}
        Online_parameters.objects.update_or_create(**params)
        return JsonResponse({"return_code": RETURN_CODE.SUCCESS, "return_msg": "新增成功"})


def delete_online_datas(request):
    """
    删除在线参数
    """
    if request.method == 'POST' and request.POST:
        id = request.POST.get('id')
        Online_parameters.objects.get(id=id).delete()
        return JsonResponse({"return_code":RETURN_CODE.SUCCESS, "return_msg":"删除成功"})
    return JsonResponse({"return_code":RETURN_CODE.FAIL, "return_msg":"删除失败"})


def add_app_version(request):
    """
    添加app版本号
    """
    if request.method == 'POST' and request.POST:
        app_version = request.POST.get('app_version', '')
        appid = request.POST.get('appid')
        exist_app = Patch.objects.filter(app_version=app_version, apppack__id=appid).exists()   # 验证app版本号的唯一性
        if exist_app:
            return JsonResponse({"return_code":RETURN_CODE.FAIL, "return_msg":"App版本已存在"})
        p = Patch()
        p.app_version = app_version
        p.apppack_id = appid
        p.save()
        return JsonResponse({"return_code":RETURN_CODE.SUCCESS, "return_msg":"添加成功"})


def delete_patch(request):
    """
    删除下发补丁
    """
    if request.method == 'POST' and request.POST:
        id = request.POST.get('id')
        p = Patch.objects.get(id=id)
        p.delete()
        return JsonResponse({"return_code":RETURN_CODE.SUCCESS, "return_msg":"删除成功"})
    return JsonResponse({"return_code":RETURN_CODE.FAIL, "return_msg":"参数无效"})


def update_patch(request):
    """
    恢复、暂停补丁下发
    """
    if request.method == 'POST' and request.POST:
        id = request.POST.get('id')
        try:
            data = Patch.objects.get(id=id)
        except Patch.DoesNotExist:
            return JsonResponse({"return_code":RETURN_CODE.FAIL, "return_msg":"参数无效"})
        enbale = data.enable

        if enbale == True:
            data.enable = False
        else:
            data.enable = True
        data.save()
        return JsonResponse({"return_code":RETURN_CODE.SUCCESS, "return_msg":"修改成功"})



def add_histroy(patch_id,
                patch_version,
                old_patch_version,
                description=0,
                size=0,
                patch_name='',
                patch_path=''):
    """
    历史记录
    """
    if  old_patch_version is None:
        return
    old = Histroy.objects.filter(patch_version=patch_version).count()
    obj, iscreate = Histroy.objects.get_or_create(patch_id=patch_id,
                                                  patch_version=patch_version,
                                                  size=size,
                                                  patch_name=patch_name,
                                                  patch_path=patch_path,
                                                  description=description)


def has_new_patch(request):
    GET = request.GET.get
    version = GET('version', '')
    uid = GET('uid', '')
    patch_version = GET('patchversion', '')
    name = GET('name', '')
    try:
        if all([version, patch_version, name]):
            patch_obj = Patch.objects.filter(app_version=version,
                                             apppack__packname=name,).first()
            if patch_obj.patch_version != patch_version:
                patch_type = patch_obj.patch_type
                patch_monitoring = PatchMonitoring.objects.filter(app_version=version,
                                                                  patch_version=patch_obj.patch_version,
                                                                  app_packname=name,
                                                                  )
                if has_push_update(patch_type, request, patch_monitoring, patch_obj.create_time):
                    return JsonResponse({"version":patch_obj.patch_version,
                                        "path":patch_obj.patch_path,
                                        "size":patch_obj.size,
                                        "hash":patch_obj.patch_name})
                else:
                    return JsonResponse({"version":0})
            else:
                return JsonResponse({"version":0})
        else:
            return JsonResponse({"version":0})
    except Exception as error:
        return JsonResponse({"version":0, "error_msg":str(error)})


def return_code(request):
    """
    接收更新成功或者失败数据
    """
    url = request.path
    arg, status = url.rsplit('/', 1)
    GET = request.GET.get
    version = GET('version', '')
    uid = GET('uid', '')
    patchversion = GET('patchversion', '')
    packname = GET('name', '')
    try:
        if not all([version, patchversion, packname]):
            return JsonResponse({'return_code':'FAIL'})
        patch_obj = Patch.objects.filter(app_version=version,
                                         apppack__packname=packname,
                                         patch_version=patchversion).first()
        date_obj = datetime.datetime.now()
        date_obj = datetime.datetime.strftime(date_obj, "%Y-%m-%d %H")
        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d %H")
        obj, is_create = PatchMonitoring.objects.get_or_create(app_packname=packname,
                                                               app_version=patch_obj.app_version,
                                                               patch_version=patch_obj.patch_version,
                                                               create_time=date_obj)
        if status == "success":
            obj.success_count += 1
            obj.save()
        else:
            obj.fail_count += 1
            obj.save()
        return JsonResponse({'return_code':RETURN_CODE.SUCCESS})
    except Exception as error:
        return JsonResponse({"return_code":RETURN_CODE.FAIL, "error_msg":str(error)})


def get_patch_version(request):
    """
    返回补丁版本号
    """
    return_value = {
        'return_code':RETURN_CODE.SUCCESS,
        'return_msg':'',
        'datas':'',
    }
    if request.method == "GET":
        try:
            app_version = request.GET.get('app_version')
            app_packname = request.GET.get('app_packname')
            pm_obj = PatchMonitoring.objects.filter(app_version=app_version,
                                                    app_packname=app_packname).values_list('patch_version')
            return_value['datas'] = list(set(pm_obj))
            return JsonResponse(return_value)
        except Exception as error:
            return_value['return_code'] = RETURN_CODE.FAIL
            return_value['return_msg'] = "服务器处理错误"
            return JsonResponse(return_value)


def get_chart_data(request):
    """
    返回安卓更新监控数据
    """
    return_value = {
        'return_code':RETURN_CODE.SUCCESS,
        'return_msg':'',
        'datas':{},
    }
    if request.method == 'POST':
        POST = request.POST.get
        appid = POST('appid')
        app = AppPack.objects.get(id=appid)
        app_version = POST('app_version')
        patch_version = POST('patch_version')
        data_type = POST('data_type')
        if not all([app_version, app_version]):
            return JsonResponse(return_value)
        obj = PatchMonitoring.objects.filter(app_packname=app.packname,
                                             app_version=app_version,
                                             patch_version=patch_version).order_by("-create_time").first()
        if not obj:
            return JsonResponse(return_value)
        day_obj = obj.create_time
        day_obj = datetime.datetime.strftime(day_obj, "%Y-%m-%d")
        day_obj = datetime.datetime.strptime(day_obj, "%Y-%m-%d")
        if data_type == "day":
            if obj:
                tm_day = day_obj + datetime.timedelta(days=1)
            else:
                return JsonResponse(return_value)
        else:
            if obj:
                tm_day = day_obj + datetime.timedelta(days=1)
                day_obj = day_obj - datetime.timedelta(days=7)
            else:
                return JsonResponse(return_value)
        pm_obj = PatchMonitoring.objects.filter(app_version = app_version, 
                                                app_packname = app.packname,
                                                patch_version = patch_version, 
                                                create_time__range=(day_obj, tm_day)).order_by("create_time").values_list("create_time","success_count",'fail_count')
        fail = sum([list(i).pop(2) for i in pm_obj])
        pm_obj = [(datetime.datetime.strftime(k,"%Y-%m-%d"),v) for k,v,j in pm_obj]
        data_dict = {}
        for k,v in pm_obj:
            try: data_dict[k] += v
            except KeyError: data_dict[k] = v
        data_list = list(data_dict.items())
        return_value['datas'] = data_list
        return_value['fail'] = fail
        return JsonResponse(return_value)


def pv_log(request):
    """
    统计用户的的动作
    """
    return_value = {
    'return_code':RETURN_CODE.SUCCESS,
    'return_msg':'',
    'datas':{},
    }
    GET = request.GET.get
    version = GET('version', '')
    uid = GET('uid', '')
    patch_version = GET('patchversion', '')
    packname = GET('name', '')
    event_id = GET('eventid', '')
    patch_obj = Patch.objects.filter(
        apppack__packname=packname,
        patch_version=patch_version,
        app_version=version,
    )
    try:
        if patch_obj:
            PV_LOG.objects.create(
                user_id=uid,
                patch_id=patch_obj.first().id,
                event_id=int(event_id)
            )
            return JsonResponse(return_value)
        else:
            return_value['return_code'] = RETURN_CODE.FAIL
            return_value['return_msg'] = "patch_obj not find"
            print(return_value)
            return JsonResponse(return_value)
    except Exception as error:
        return_value['return_code'] = RETURN_CODE.FAIL
        return_value['return_msg'] = "api error"
        print(return_value)
        return JsonResponse(return_value)

