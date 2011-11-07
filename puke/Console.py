import logging, sys
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
		console.error(" /!\\ BUILD FAIL : " + msg)
		sys.exit(1)


