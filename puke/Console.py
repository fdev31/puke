import logging, sys, os
from colorama import *

init(autoreset = True)

class console:
	

	@staticmethod
	def log(msg):
		if os.environ.get("NOCOLOR"):
			logging.info(  msg)
		else:
			logging.info( Style.BRIGHT + msg)
	
	@staticmethod
	def info(msg):
		logging.info(   msg)

	@staticmethod
	def debug(msg):
		if os.environ.get("NOCOLOR"):
			logging.debug( msg )
		else:
			logging.debug( Back.BLUE +  msg )

	@staticmethod
	def warn(msg):
		
		msg = console.pukefactory(msg)
		if os.environ.get("NOCOLOR"):
			logging.warning(  msg)
		else:
			logging.warning( Fore.YELLOW + Style.BRIGHT + msg)
	
	@staticmethod
	def error(msg):
		if os.environ.get("NOCOLOR"):
			logging.error(  msg)
		else:
			logging.error( Back.RED + Style.BRIGHT + msg)

	@staticmethod
	def confirm(msg):
		if os.environ.get("NOCOLOR"):
			logging.info(msg )
		else:
			logging.info(Fore.GREEN + Style.BRIGHT + msg )
	
	@staticmethod
	def header(msg, level = 2):
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



