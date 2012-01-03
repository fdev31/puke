#!/usr/bin/env python
# -*- coding: utf8 -*-

import logging, sys, os, json
from colorama import *

init(autoreset = True)

class console:
	


	@staticmethod
	def log(*messages):
		color = Style.BRIGHT 
		if os.environ.get("NOCOLOR"):
			color = ""

		for m in messages:
			msg = console.stringify(m)
			logging.info(color + msg)
	
	@staticmethod
	def info(*messages):
		for m in messages:
			msg = console.stringify(m)
			logging.info(   msg)

	@staticmethod
	def debug(*messages):
		color = Back.BLUE

		if os.environ.get("NOCOLOR"):
			color = ""
		
		if os.environ.get("NOCOLOR"):
			color = ""

		for m in messages:
			msg = console.stringify(m)
			logging.debug( color +  msg )

	@staticmethod
	def warn(*messages):
		color = Fore.YELLOW + Style.BRIGHT

		if os.environ.get("NOCOLOR"):
			color = ""

		for m in messages:
			msg = console.stringify(m)
			msg = console.pukefactory(msg)
		
			logging.warning( color + msg)
	
	@staticmethod
	def error(*messages):
		color = Back.RED + Style.BRIGHT

		if os.environ.get("NOCOLOR"):
			color = ""

		for m in messages:
			msg = console.stringify(m)
			logging.error( color + msg)

	@staticmethod
	def confirm(*messages):
		color = Fore.GREEN + Style.BRIGHT

		if os.environ.get("NOCOLOR"):
			color = ""
			
		for m in messages:
			msg = console.stringify(m)
			logging.info(color + msg )
	
	@staticmethod
	def header(msg, level = 2):
		msg = console.stringify(msg)
		logging.info("")
		if level == 1:
			color = Fore.MAGENTA
		else:
			color = Fore.CYAN
		
		if os.environ.get("NOCOLOR"):
			logging.info(msg )
		else:
			logging.info(color + Style.BRIGHT + msg )

	@staticmethod
	def fail(msg):
		msg = console.stringify(msg)
		msg = console.pukefactory(msg)
		console.error(" /!\\ BUILD FAIL : " + msg)
		sys.exit(1)

	@staticmethod
	def pukefactory(msg):
		if ':puke:' in msg:
			try:
				f = open(os.path.join(os.path.dirname( __file__ ), 'datas','decoration', 'puke.txt'), 'r')
				msg = msg.replace(':puke:', '\n' + f.read())
				f.close()

				return msg
			except Exception:
				pass
		
		return msg


	@staticmethod
	def stringify(msg):
		if isinstance(msg, str):
			return msg

		return json.JSONEncoder().encode(msg)
