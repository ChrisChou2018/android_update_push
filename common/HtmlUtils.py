# -*- coding: utf-8 -*-

"""
"""

import urllib.parse

class Attrs:
	"""
	"""
	def __init__(self, *args, **kw):
		self.kw = list(args) + list(kw.items())
	
	def __str__(self):
		return " ".join(['%s="%s"' % (urllib.parse.quote(k), urllib.parse.quote(str(v))) for k, v in self.kw])
	
	def __setitem__(self, k, v):
		self.kw[k] = v
	
	def __getitem__(self, k):
		return self.kw[k]

class Tag(object):
	"""
	"""
	TAG = ""
	
	def __init__(self, val = "", **kw):
		"""
		"""
		self.attrs = Attrs(**kw)
		self.val = val
		self.tags = []

	def tag(self, t):
		"""
		"""
		self.tags.append(t)
		return t

	def __str__(self):
		"""
		"""
		attrs = str(self.attrs)
		result = [ attrs and "<%s %s>" % (self.TAG, attrs) or "<%s>" % self.TAG]
		tags = "\n".join([str(e) for e in self.tags])
		
		if callable(self.val):
			val = str(self.val())
		else:
			val = str(self.val)
		
		if tags:
			result.append(val + "\n" + tags + "\n")
		else:
			result.append(val)
		
		result.append("</%s>" % self.TAG)
		return "".join(result)

class TH( Tag ):
	TAG = "th"

class TD( Tag ):
	TAG = "td"

class TR( Tag ):
	TAG = "tr"
	
	def th(self, val = "", **kw):
		"""
		"""
		th = TH(val, **kw)
		self.tags.append(tr)
		return th

	def td(self, val = "", **kw):
		"""
		"""
		td = TD(val, **kw)
		self.tags.append(td)
		return td

	def tds(self, *args, **kw):
		"""
		tr.tds("val1", "val2", ..., "valN", attr1 = xxx, attr2 = yyy)
		"""
		tds = [TD(v, **kw) for v in args]
		self.tags.extend(tds)
		return tds



class Table(Tag):
	"""
	输出数据到html的table
	"""
	TAG = "table"
	
	def tr(self, val = "", **kw):
		"""
		"""
		tr = TR(val, **kw)
		self.tags.append(tr)
		return tr
	


"""
table = HtmlUtils.Table(border = 1)
for e1 in range(10):
    tr = table.tr()
    for e2 in range(5):
        tr.td("%s - %s" % (e1, e2))
print(table)
"""
