#!/usr/bin/env python
# -*- coding: utf8 -*-

class Yak(dict):

	class __metaclass__(type):
		def __iter__(self):
			for attr in dir(Yak):
				if not attr.startswith("__"):
					yield attr
	@staticmethod
	def set(key, value):
		setattr(Yak, key, value)

	@staticmethod
	def get(key, default = None):
		try:
			return getattr(Yak, key)
		except:
			return default
