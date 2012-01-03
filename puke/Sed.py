#!/usr/bin/env python
# -*- coding: utf8 -*-

import hashlib

class Sed:

	def __init__(self):
		self._list = {}

	def add(self, search, replace):
		self._list[search] = replace

	def keys(self):
		t = []
		for k,v in self._list.items():
			t.append(k)
		return t
	
	def get(self, key):
		return self._list[key]

	def getSignature(self):
		sig = ""
		for k,v in self._list.items():
			sig += "%s" % hashlib.sha256("%s%s" % (k,v)).hexdigest()

		return hashlib.sha256(sig).hexdigest()