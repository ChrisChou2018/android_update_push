import datetime, urllib, time, random
import hashlib
import json
from common.Define import RETURN_CODE
from django import forms
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, JsonResponse)
from django.conf import settings
from django.contrib import messages
from django.db.models import F
from django.db.models import Count, Max
from .models import (Online_parameters, Patch, Histroy, AppPack, PatchMonitoring)
from .views_api import add_histroy
import os



def index(request):
    """
    我的App首页
    """
    allapp = AppPack.objects.all()
    context = { "allapp" : allapp}
    return render(request, "main/index.html", context)


def add_app(request):
    """
    添加App
    """
    return render(request, "main/add_app.html")


def patch_issued(request, appid):
    """
    补丁下发
    """
    app = AppPack.objects.get(id = appid)
    patchs = Patch.objects.filter(apppack = appid)
    context = { "patchs" : patchs, "app" : app }
    return render(request, "main/patch_issued.html", context)


def add_app_version(request, appid):
    """
    添加app版本
    """
    app = AppPack.objects.get(id = appid)
    context = {"app" : app}
    return render(request, "main/add_app_version.html", context)


def add_patch(request, appid, id):
    """
    发布补丁
    """
    app = AppPack.objects.get(id = appid)
    if not id:
        return HttpResponseRedirect('/main/')
    if request.method == 'POST':
        POST = request.POST.get
        patch = request.FILES.get('patch', None)
        if not patch:
            return HttpResponseRedirect('/main/%s/%s/add_patch.do' % (appid, id))
        myhash = hashlib.md5()
        with open((settings.LOCALS_PATCH_PATH + patch.name), 'wb+') as f:
            for chunk in patch.chunks():
                myhash.update(chunk)
            new_file_name = myhash.hexdigest()
            if not os.path.isfile(settings.LOCALS_PATCH_PATH + new_file_name):
                for chunk in patch.chunks():
                    f.write(chunk)
        if not os.path.isfile(settings.LOCALS_PATCH_PATH + new_file_name):
            os.rename(settings.LOCALS_PATCH_PATH + patch.name,settings.LOCALS_PATCH_PATH + new_file_name)
        patch_type = POST("patch_type")
        if patch_type == "condition":
            conditionValue = POST('conditionValue')
            patch_type += (":"+conditionValue)
        elif patch_type == "gray":
            grayType = POST('grayType')
            grayValue = POST('percentageCount') if grayType == "percentage" else POST('count')
            time_out = POST('time_out') if grayType == "percentage" else ''
            patch_type += (":"+grayType+"="+grayValue)
            if time_out:
                patch_type += "&time_out={0}".format(time_out)
        id = int(id)
        qs = Patch.objects.get(id = id)
        old_patch_version = qs.patch_version
        old_patch_name = qs.patch_name
        old_patch_path = qs.patch_path
        ole_patch_type = qs.patch_type
        qs.description = POST('description', '')
        qs.patch_name = myhash.hexdigest()
        qs.patch_type = patch_type
        qs.patch_path = settings.SERVER_PATCH_PATH + new_file_name
        qs.patch_version = POST("patch_version", "")
        qs.issued += 1
        qs.size = int(patch.size/1000)
        qs.save()
        add_histroy(id, 
                    POST("patch_version", ""), 
                    old_patch_version, 
                    POST('description', ''), 
                    size = int(patch.size/1000), 
                    patch_name = old_patch_name, 
                    patch_path = old_patch_path,)
        return HttpResponseRedirect('/main/%s/%s/patch_details.do' % (appid, id) )
    else:
        parameters_obj = Online_parameters.objects.all()
        datas = Patch.objects.get(id = id)
        context = { "datas" : datas, "app" : app , "pm_obj":parameters_obj}
        return render(request, "main/add_patch.html", context)




def patch_details(request, id, appid):
    """
    补丁下发详情
    """
    app = AppPack.objects.get(id = appid)
    if not id:
        return HttpResponseRedirect('/main/')
    datas = Patch.objects.get(id = id)
    context = {"datas": datas, "app" : app }
    if datas.app_version:
        return render(request, "main/patch_details.html", context)
    else:
        return HttpResponseRedirect(reverse("add_patch", args = {datas.id}))




def online_datas(request, appid):
    """
    在线参数
    """
    app = AppPack.objects.get(id = appid)
    datas = Online_parameters.objects.all()
    context = { "datas" : datas, "app" : app }

    return render(request, "main/online_datas.html", context)


def monitor(request, appid):
    """
    实时监控
    """
    app = AppPack.objects.filter(id=appid).first()
    context = {"app" : app}
    return render(request, "main/monitor.html", context )


def histroy(request, appid):
    """
    历史补丁
    """ 
    app = AppPack.objects.get(id = appid)
    qs = Patch.objects.filter(apppack=app.id).order_by('id')
    context = ((i, (j for j in i.histroy_set.all())) for i in qs)
    return render(request, "main/histroy.html",context = {'context' : context, "app" : app })


def histroy_details(request, id, appid):
    """
    历史补丁详情
    """
    app = AppPack.objects.get(id = appid)
    datas = Histroy.objects.get(id = id,patch__apppack=app.id)
    app_version = Patch.objects.get(id = datas.patch.id).app_version
    context = { "datas" : datas, "app_version" : app_version, "app" : app }
    return render(request, "main/histroy_details.html", context)


def app_information(request, appid):
    """
    app信息
    """
    app = AppPack.objects.get(id = appid)
    if  request.method == 'GET':
        context = {"app" : app }
        return render(request, "main/app_information.html", context)
    else:
        method = request.POST.get('method')
        if  method == 'update':
            appname = request.POST.get('appname')
            packname = request.POST.get('packname')
            if not appname or not packname:
                return render(request,"main/app_information.html",{"return_msg":"app名称和包名都不可为空",'app':app})
            exist_appname = AppPack.objects.filter(appname=appname).exists()                    # 验证app名称的唯一性
            if exist_appname:
                return render(request,"main/app_information.html",{"return_msg" : "app名称已存在或无修改","app":app})
            else:
                AppPack.objects.filter(id=appid).update(appname=appname,packname=packname)
                return redirect(reverse('app_information',kwargs={'appid':appid}))
        else:
            app.delete()
            return redirect(reverse('index'))








