# -*- coding: utf-8 -*-

"""
工具代码
"""
import hashlib, math, datetime, os, sys, json, random, string, time, itertools, base64
import urllib.request, urllib.parse, http.cookiejar
from django.http import HttpResponse

from . import pyDes

import logging

logger = logging.getLogger("default")


# 空类
class Object(object):
	def __init__(self, *args, **kwargs):
		self.__dict__.update(list(args) + list(kwargs.items()))


def Redirect(fullurl, data=None, cookieJar=None):
	"""
	重定向访问指定的网页
	@param fullurl: 完整的可以在浏览器的地址栏中使用的网址
	@param data: 如果这个值非None，必须以类似于“[("key", "value"), ...]”的格式提供数据，
	             这时将会以 post 模式访问，否则以 get 模式访问。
	@param cookieJar: 用于存放cookie的实例，如果不想保留cookie数据用于后续使用，此参数可以不提供。
	@return: string, 返回网页访问结束后读取的数据
	"""
	if cookieJar is None:
		cookieJar = http.cookiejar.CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))
	# opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:2.0) Gecko/20100101 Firefox/4.0')]
	if data is not None:
		data = urllib.parse.urlencode(data)

	try:
		response = opener.open(fullurl, data)
	except Exception as errstr:
		logger.error("%s" % fullurl)
		raise errstr
	return response.read()


def DatetimeStr():
	"""
	YYYYmmddHHMMSS -> '20170606112826'
	@return: string
	"""
	return time.strftime("%Y%m%d%H%M%S", time.localtime())


def FormatDatetime():
	"""
	%Y-%m-%d %H:%M:%S -> '2017-11-15 16:29:42'
	"""
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class _UIDMaker:
	"""
	uid生成器
	"""

	def __init__(self):
		"""
		@parame prefix: uid前缀字符串
		"""
		self.prepStr = "%s" + "%05u" % os.getpid() + "%05u"
		self._auto_id = 0  # 局计数，0xFFFF一轮回

	def make(self, prefix=""):
		"""
		make new id
		"""
		t = time.time()
		st = time.strftime("%Y%m%d%H%M%S", time.localtime(t)) + "%03d" % int(t * 1000 % 1000)
		self._auto_id = self._auto_id % 0xFFFF + 1
		return prefix + self.prepStr % (st, self._auto_id)

	def makeINT64(self):
		"""
		生成一个64位的纯整数uid
		"""
		self._auto_id = self._auto_id % 0xFFFF + 1
		return (int(time.time() * 1000) << 16) + self._auto_id

	def __call__(self, prefix=""):
		"""
		@return: string
		UM = UIDMaker("abc")
		UM()
		abc201706061103426061001200001
		"""
		return self.make(prefix)


UIDMaker = _UIDMaker()


def PrintStack():
	"""
	打印当前堆栈调用信息，用于调试
	"""
	frame = sys._getframe().f_back
	print("<Debug> Stack trace:")
	print("(From file %s, line %s, in %s)" % traceback.extract_stack(frame, 1)[0][:3])
	traceback.print_stack(frame)


def MakeSortedUri(*args, **kws):
	"""
	通过传递进来的参数，生成一条排序过的uri参数
	"""
	vl = list(args) + list(kws.items())
	vl.sort(key=lambda x: x[0])
	sl = ["%s=%s" % (e[0], e[1]) for e in vl]
	uri = "&".join(sl)
	return uri


class Page(object):

	def __init__(self, rowAmount, pageIdx, amountPerPage):
		"""
		@param     rowAmount: INT；数据总量
		@param       pageIdx：INT；当前页数
		@param amountPerPage：INT；每页的数量
		"""
		self.rowAmount = rowAmount
		self.pageIdx = pageIdx
		self.amountPerPage = amountPerPage
		self.pages = math.ceil(self.rowAmount / self.amountPerPage)

	def __repr__(self):
		return '<Page %s of %s>' % (self.pageIdx, self.pages)

	def has_next(self):
		return self.pageIdx < self.pages

	def has_previous(self):
		return self.pageIdx > 1

	def has_other_pages(self):
		return self.has_previous() or self.has_next()

	def next_page_number(self):
		return self.pageIdx < self.pages and self.pageIdx + 1 or self.pages

	def previous_page_number(self):
		return self.pageIdx > 1 and self.pageIdx - 1 or 1

	def start_index(self):
		"""
		"""
		# Special case, return zero if no items.
		if self.rowAmount == 0:
			return 0
		return self.amountPerPage * (self.pageIdx - 1)

	def end_index(self):
		"""
		"""
		# Special case for the last page because there can be orphans.
		if self.pageIdx >= self.pages:
			return self.rowAmount
		return self.amountPerPage * self.pageIdx

	def showList(self):
		"""
		生成显示列表
		"""
		offset = 5
		rHead = []
		rTail = []
		startIdx = self.pageIdx - offset
		if startIdx <= 2:
			startIdx = 1
		else:
			rHead = [1, "..."]

		endIdx = self.pageIdx + offset
		if endIdx > self.pages - 2:
			endIdx = self.pages
		else:
			rTail = ["...", self.pages]

		rBody = list(range(startIdx, endIdx + 1))
		return rHead + rBody + rTail


g_STR_WORLD = string.ascii_letters + string.digits


def RandStr(strLen, seed=g_STR_WORLD):
	"""
	生成随机位数的字符串
	@param strLen: 字符串长度
	"""
	assert strLen > 0
	l = len(seed) - 1
	vs = [seed[random.randint(0, l)] for i in range(strLen)]
	return "".join(vs)


g_PASSWD_WORLD = string.ascii_letters + string.digits + "`~!@#$%^&*()_+-=[]{};:|,.<>?"


def RandPassword(pwdLen, seed=g_PASSWD_WORLD):
	"""
	生成随机位数的密码
	@param pwdLen: 密码长度
	"""
	return randStr(pwdLen, seed)


def Signature(secret, *args, **kwargs):
	"""
	把args中的数据与 secret 组合生成签名（校验码）

	◆ 参数名ASCII码从小到大排序（字典序）；
	◆ 如果参数的值为空不参与签名；
	◆ 参数名区分大小写；

	@param secret: 签名时所用的key
	"""
	argD = dict(args)
	argD.update(kwargs)

	vs = list(argD.items())
	vs.sort(key=lambda x: x[0])
	rs = ["%s=%s" % (k, v) for k, v in vs if (v != None and v != "")]
	rs.append("key=%s" % secret)
	s = "&".join(rs)

	m = hashlib.md5(s.encode())
	d = m.hexdigest()
	return d.upper()


def GetCurrentYYYYMM():
	"""
	返回当前的处理时间标识，这个值用于processTime字段
	"""
	today = datetime.date.today()
	return today.year * 100 + today.month


def GetCurrentYYYYMMDD():
	"""
	返回当前的处理时间标识，这个值用于processTime字段
	"""
	today = datetime.date.today()
	return today.year * 10000 + today.month * 100 + today.day


def DateOffsetByMonth(datetime1, n=1):
	"""
	把datetime或date实例偏移n个月
	"""
	# create a shortcut object for one day
	one_day = datetime.timedelta(days=1)

	# first use div and mod to determine year cycle
	q, r = divmod(datetime1.month + n, 12)

	# create a datetime2 to be the last day of the target month
	if isinstance(datetime1, datetime.datetime):
		datetime2 = datetime.datetime(datetime1.year + q, r + 1, 1, datetime1.hour, datetime1.minute, datetime1.second,
		                              datetime1.microsecond)
	else:
		datetime2 = datetime.date(datetime1.year + q, r + 1, 1)

	datetime2 -= one_day

	"""
	if input date is the last day of this month
	then the output date should also be the last
	day of the target month, although the day
	www.iplaypy.com
	may be different.
	for example:
	datetime1 = 8.31
	datetime2 = 9.30
	"""

	if datetime1.month != (datetime1 + one_day).month:
		return datetime2

	"""
	if datetime1 day is bigger than last day of
	target month, then, use datetime2
	for example:
	datetime1 = 10.31
	datetime2 = 11.30
	"""

	if datetime1.day >= datetime2.day:
		return datetime2

	"""
	then, here, we just replace datetime2's day
	with the same of datetime1, that's ok.
	"""

	return datetime2.replace(day=datetime1.day)


def OneDayRange(datetime1=None):
	"""
	转换给定时间所在的一天以内的时间范围
	@return (begin_datetime, end_datetime)
	"""
	if not datetime1:
		datetime1 = datetime.date.today()
	begin_datetime = datetime.datetime(datetime1.year, datetime1.month, datetime1.day, 0, 0, 0)
	return (begin_datetime, begin_datetime + datetime.timedelta(days=1))


def CalcLastDayOfMonth(date=None):
	"""
	计算某月的最后一天

	@return: INT
	"""
	if not date:
		date = datetime.date.today()
	d = DateOffsetByMonth(date)
	d = datetime.date(d.year, d.month, 1) - datetime.timedelta(days=1)
	return d.day


def djmodel_to_object(instance, fields=None, exclude=None):
	"""
	把Model实例转换成纯对象实例——某些时候我们并不想向外提供如Model.save()的时候可以使用

	``fields`` is an optional list of field names. If provided, only the named
	fields will be included in the returned dict.

	``exclude`` is an optional list of field names. If provided, the named
	fields will be excluded from the returned dict, even if they are listed in
	the ``fields`` argument.
	"""
	opts = instance._meta
	data = {}
	for f in itertools.chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
		if fields and f.name not in fields:
			continue
		if exclude and f.name in exclude:
			continue
		data[f.name] = f.value_from_object(instance)
	o = Object(**data)
	return o


def CheckQuerySign(secret, request, sign_key="sign"):
	"""
	计算并检查request下的签名是否正确

	@return: bool；True - 签名相同
	"""
	d = request.GET.dict()
	q_sign = d.pop(sign_key)  # 数字签名
	sign = Signature(secret, **d)
	return sign.lower() == q_sign.lower()


class TimeTrack(object):
	"""
	运行时间跟踪
	"""

	def __init__(self):
		"""
		"""
		self.start()

	def start(self):
		"""
		"""
		self.t = time.time()

	def stop(self):
		"""
		"""
		return time.time() - self.t


def build_absolute_uri(request, url):
	"""
	把相对地址转换成绝对地址
	"""
	if not url:
		return ""
	if not url.startswith("http"):
		return request.build_absolute_uri(url)
	return url


def split_absolute_uri(url):
	"""
	去除绝对地址的查询字符串
	@return : a url but not have query string
	"""
	s_url = url.split("?")
	return str(s_url[0])

def des3_encrypt(key, data):
	"""
	3des加密
	@todo(phw): 这里以后要优化，当在linux下时，应该使用pycrypto库才更有效率
	"""
	if not isinstance(key, bytes):
		key = key.encode("utf-8")
	if not isinstance(data, bytes):
		data = data.encode("utf-8")
	m = pyDes.triple_des(key, pyDes.ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
	return m.encrypt(data)

def des3_decrypt(key, data):
	"""
	3des解密
	@todo(phw): 这里以后要优化，当在linux下时，应该使用pycrypto库才更有效率
	"""
	if not isinstance(key, bytes):
		key = key.encode("utf-8")
	if not isinstance(data, bytes):
		data = data.encode("utf-8")
	m = pyDes.triple_des(key, pyDes.ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
	return m.decrypt(data)

def des3_encrypt_base64(key, data):
	"""
	3des加密，并转成base64数据
	"""
	#return base64.encodebytes(des3_encrypt(key, data))
	return base64.urlsafe_b64encode(des3_encrypt(key, data))

def des3_decrypt_base64(key, data):
	"""
	从base64中还原后再用3des解密数据
	"""
	#if not isinstance(data, bytes):
	#	data = data.encode("utf-8")
	data = base64.urlsafe_b64decode(data)
	return des3_decrypt(key, data)
