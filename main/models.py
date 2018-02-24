# -*- coding: utf-8 -*-
import datetime
from django.db import models
from common.Define import EVENT_CHOICES


class AppPack(models.Model):
	"""
	App包
	"""
	id 			= models.AutoField(primary_key = True)
	appname 	= models.CharField( "app名称", db_column = 'c_appname', max_length = 64, unique = True, blank = False, null = False, help_text = "app的名称" )
	packname 	= models.CharField( "包名", db_column = 'c_packname', max_length = 64, unique = True, blank = False, null = False, help_text = "包名" )

	class Meta:
		verbose_name 		= "AppPack：App包"
		verbose_name_plural = "AppPack：App包"

class Online_parameters(models.Model):
	"""
	在线参数
	"""
	id 		= models.AutoField(primary_key = True)
	pname 	= models.CharField( "参数名称", db_column = "c_pname", max_length = 255, blank = False, null = False, help_text = "参数名称" )
	pvalues = models.CharField( "参数值", db_column = "c_pvalues", max_length = 255, blank = False, null = False, help_text = "参数值" )

	class Meta:
		verbose_name 		= "Online_parameters：在线参数表"
		verbose_name_plural = "Online_parameters：在线参数表"


class Patch(models.Model):
	"""
	补丁下发详情
	"""
	id 				= models.AutoField(primary_key = True)
	app_version 	= models.CharField( "APP的版本", db_column = "c_app_version",default = '', max_length = 64, help_text = "APP的版本" )
	patch_name		= models.CharField( "补丁包名字", db_column = "c_patch_name", max_length = 255, null = True,	blank = True, help_text = "补丁包的名字为补丁文件哈希值")
	size 			= models.IntegerField( "补丁大小", db_column = "c_size", default = 0,  help_text = "补丁大小" )
	patch_path		= models.CharField("补丁的路径", db_column = "补丁文件的路径", max_length = 255, null = True,	blank = True, help_text = "补丁包的路径")
	issued 			= models.IntegerField( "已下发补丁", db_column = "c_issued", default = 0, help_text = "已下发补丁")
	apppack 		= models.ForeignKey( AppPack, models.CASCADE, verbose_name = '所属的App', db_column = 'c_apppack_id', blank = False, null = False, help_text= '所属的App', default="")
	patch_version 	= models.CharField( "当前补丁版本", db_column = "c_patch_version", max_length = 255, null = True, blank = True, help_text = "当前补丁版本，默认为0,不在历史补丁页面上显示" )
	description 	= models.TextField( "补丁描述", db_column = "c_description", null = True, blank = True, default = "" )
	enable 			= models.BooleanField( "当前补丁下发状态", db_column = "c_enable", default = True, help_text = "补丁下发状态，默认已下发，否则显示未下发" )
	patch_type		= models.CharField("补丁类型", db_column="c_patch_type", default="", max_length=64, help_text="all全部, percentage:10按百分比10, kwarg:k=v按参数k=v")
	create_time 	= models.DateTimeField( "创建时间", db_column = "c_create_time", auto_now_add = True )
	modified_time 	= models.DateTimeField( "修改时间", db_column = "c_modified_time", auto_now = True )

	class Meta:
		verbose_name 		= "Patch：补丁下发表详情"
		verbose_name_plural = "Patch：补丁下发表详情"
		unique_together = ('app_version', 'apppack',)




class Histroy(models.Model):
	"""
	历史补丁
	"""
	id 				= models.AutoField(primary_key = True)
	size 			= models.IntegerField("当前补丁大小", db_column="c_size", default=0, help_text="当前补丁大小")
	patch_version 	= models.CharField("补丁版本", db_column="c_patch_version", max_length = 255, default = "", help_text="补丁版本，默认为1")
	patch 			= models.ForeignKey(Patch,verbose_name = "所属app版本", db_column = "c_patch_id", blank = True, null = True, help_text = "所属app版本" )
	patch_name		= models.CharField( "补丁包名字", db_column = "c_patch_name", max_length = 255, null = True,	blank = True, help_text = "补丁包的名字，未哈希值" )
	patch_path 		= models.CharField("补丁路径", db_column = "c_patch_path", max_length = 255, null = True,	blank = True, help_text = "补丁包的路径")
	description 	= models.TextField( "补丁描述", db_column = "c_description", null = True, blank = True, default = "" )
	patch_type		= models.CharField("补丁类型", db_column="c_patch_type", default="", max_length=64, help_text="all全部, percentage:10按百分比10, kwarg:k=v按参数k=v")
	create_time 	= models.DateTimeField( "创建时间", db_column = "c_create_time", auto_now_add = True )
	modified_time 	= models.DateTimeField( "修改时间", db_column = "c_modified_time", auto_now = True )

	class Meta:
		verbose_name 		= "Histroy：历史补丁"
		verbose_name_plural = "Histroy：历史补丁"



class PatchMonitoring(models.Model):
	"""
	更新反馈
	"""
	app_version 	= models.CharField( "APP的版本", db_column = "c_app_version", default = '', max_length = 64, help_text = "APP的版本" )
	app_packname	= models.CharField( "APP包名", db_column = "c_app_pack_name", max_length = 255, null = True, blank = True, )
	patch_version 	= models.CharField( "当前补丁版本", db_column = "c_patch_version", max_length = 255, null = True, blank = True, help_text = "当前补丁版本，默认为0,不在历史补丁页面上显示" )
	success_count 	= models.IntegerField("补丁成功数",db_column = "c_success_count", default=0)
	fail_count 		= models.IntegerField("补丁失败数", db_column = "fail_count" , default=0)
	create_time 	= models.DateTimeField( "创建时间", db_column = "c_create_time", auto_now_add = True )
	modified_time 	= models.DateTimeField( "修改时间", db_column = "c_modified_time", auto_now = True )



class PV_LOG(models.Model):
	"""
	用户动作记录表
	"""
	user_id 		= models.CharField("用户ID", db_column="c_user_id", null=True, max_length=255)
	patch_id 		= models.CharField("补丁版本ID", db_column="c_patchid", null=True, max_length=255)
	event_id		= models.IntegerField("事件ID", db_column="c_event_id", default=0, choices=EVENT_CHOICES)
	create_time 	= models.DateTimeField( "创建时间", db_column = "c_create_time", auto_now_add = True )
	modified_time 	= models.DateTimeField( "修改时间", db_column = "c_modified_time", auto_now = True )
