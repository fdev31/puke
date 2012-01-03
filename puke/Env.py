#!/usr/bin/env python
# -*- coding: utf8 -*-

import os

class Env:

	@staticmethod
	def get(name, default):
		v = os.environ.get(name)

		if not v:
			return default
		
		return v