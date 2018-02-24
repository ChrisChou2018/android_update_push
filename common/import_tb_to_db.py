import openpyxl
from django.conf import settings
import re
from importlib import import_module
import logging



def import_table_to_database(xlsfile,
                             app,
                             table_name=None,
                             clearTable=False,
                             cmd=False):
	"""
	负责将表文件数据迁移至数据库
	@param xlsfile：导入表的路径
	@param app：导入到哪个app的model下
	@param table_name: 是否限制表级别的导入
	@param clearTable：是否导入前将表清空
	@param cmd: 是否命令端调用
	"""
	if cmd:
		logger = logging.getLogger("command")
	else:
		logger = logging.getLogger("default")
	
	wb = openpyxl.load_workbook(xlsfile, read_only=False)
	valid_app_name_checker = re.compile("^[a-zA-Z][a-zA-Z0-9_]*")
	# 遍历所有的sheet
	for sheet in wb.worksheets:
		tblName = sheet.title.split("(")[0]
		if table_name:
			if table_name != tblName:
				raise Exception('导入的表不是对应的数据,请查看文件中是否还有别的数据表')
		# 不符合规则
		if not valid_app_name_checker.match(tblName):
			logger.error("invalid app name '%s'." % (tblName))
			continue

		modelsPath = app + ".models"
		m = import_module(modelsPath)
		cls = getattr(m, tblName, None)
		# 不存在相对应的配置表则忽略
		if not cls:
			logger.error("class '%s' not found in '%s', ignore." %
			             (tblName, modelsPath))
			continue
		logger.info("importing '%s' - '%s' into '%s.%s'..." %
		            (sheet.title, tblName, modelsPath, tblName))
		if clearTable:
			cls.objects.all().delete()

		values = sheet.values
		keys = next(values)
		descs = next(values)

		orms = []

		for e in values:
			# logger.debug("process row - '%s'" % str(e))
			if e[0] is None:
				logger.info("ignore row '%s'" % str(e))
				continue
			d = dict([(k, v) for k, v in zip(keys, e)
			          if v is not None and k and hasattr(cls, k)])

			orms.append(cls(**d))

		cls.objects.bulk_create(orms, 100)
		logger.info("import data %s rows" % len(orms))
