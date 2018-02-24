# -*- coding: utf-8 -*-

import threading

class Singleton(object):
	"""
	单件
	来自：http://www.cnblogs.com/tqsummer/archive/2011/01/24/1943315.html
	"""
	objs  = {}
	objs_locker =  threading.Lock()

	def __new__(cls, *args, **kv):
		if cls in cls.objs:
			return cls.objs[cls]['obj']

		cls.objs_locker.acquire()
		try:
			if cls in cls.objs: ## double check locking
				return cls.objs[cls]['obj']
			obj = object.__new__(cls)
			cls.objs[cls] = {'obj': obj, 'init': False}
			setattr(cls, '__init__', cls.decorate_init(cls.__init__))
		finally:
			cls.objs_locker.release()
		return cls.objs[cls]['obj']
   
	@classmethod
	def decorate_init(cls, fn):
		def init_wrap(*args):
			if not cls.objs[cls]['init']:
				fn(*args)
				cls.objs[cls]['init'] = True
			return

		return init_wrap
