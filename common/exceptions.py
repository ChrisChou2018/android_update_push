# -*- coding: utf-8 -*-

"""
异常定义
"""

class UBoxException(Exception):
	"""
	异常模块
	"""

	def __init__(self, errcode, errmsg):
		"""
		@param errcode: 错误码；RETURN_CODE.*
		@param errmsg: 错误描述
		"""
		self.errcode = errcode
		self.errmsg = errmsg

	def __str__(self):
		return 'Error code: {code}, message: {msg}'.format(
			code = self.errcode,
			msg = self.errmsg
		)

	def __repr__(self):
		return '{klass}({code}, {msg})'.format(
			klass = self.__class__.__name__,
			code = self.errcode,
			msg = self.errmsg
		)
