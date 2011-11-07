import logging, sys, os
from colorama import *

init(autoreset = True)

class console:
	

	@staticmethod
	def log(msg):
		logging.info( Style.BRIGHT + msg)
	
	@staticmethod
	def info(msg):
		logging.info(   msg)

	@staticmethod
	def debug(msg):

		logging.debug( Back.BLUE +  msg )

	@staticmethod
	def warn(msg):
		
		msg = console.pukefactory(msg)
		logging.warning( Fore.YELLOW + Style.BRIGHT + msg)
	
	@staticmethod
	def error(msg):
		logging.error( Back.RED + Style.BRIGHT + msg)

	@staticmethod
	def confirm(msg):
		logging.info(Fore.GREEN + Style.BRIGHT + msg )
	
	@staticmethod
	def header(msg, level = 2):
		logging.info("")
		if level == 1:
			color = Fore.MAGENTA
		else:
			color = Fore.CYAN

		logging.info(color + Style.BRIGHT + msg )

	@staticmethod
	def fail(msg):
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



