# -*- coding: utf-8 -*-
from django.conf import settings

from common import Utils
def MakeUID():
	return Utils.UIDMaker(settings.UID_PREFIX)

def MakeNoPrefixUID():
	return Utils.UIDMaker()

