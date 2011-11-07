import os, logging
import fnmatch, re

class FileList:

	def __init__(self, dir, filter = "", exclude = ""):
		self.__list = []
		self.__dir = dir
		self.__filter = ""


		for tmp_f in filter.split(','):
			tmp_f = tmp_f.strip(' ')
			self.__filter = "%s|(%s)" % (self.__filter, fnmatch.translate(tmp_f))
		
		self.__filter = self.__filter.strip('|')
		self.__filter = re.compile(self.__filter)
		
		self.__exclude = ""
		for tmp_f in exclude.split(','):
			tmp_f = tmp_f.strip(' ')
			self.__exclude = "%s|(%s)" % (self.__exclude, fnmatch.translate(tmp_f))
		
		self.__exclude = self.__exclude.strip('|')
		self.__exclude = re.compile(self.__exclude)



		self.__explore(dir)
	
	def get (self):
		return self.__list

	def __explore(self, dir ):
	    dir = os.path.abspath(dir)
	    for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
	        nfile = os.path.join(dir,file)
	        
	        if os.path.isdir(nfile):
	            self.__explore(nfile)
	        elif self.__filter.match(nfile) and not self.__exclude.match(nfile):
	        	self.__list.append(nfile)
	        