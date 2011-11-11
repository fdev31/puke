import os, logging
import fnmatch, re
import urllib2
import hashlib

from puke.Console import *
from puke.FileSystem import *



class FileList:

	def __init__(self, dir, filter = "*", exclude = ""):
		self.__list = []
		self.__dir = dir
		self.__filter = ""


		if dir.startswith('http'):
			self.__list.append((dir,''))
			return


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

	def merge (self, flist):
		if isinstance(flist, FileList):
			flist = flist.get(True)
		elif isinstance(flist, str):
			flist = [(flist, '')]
		else:
			result = []
			for f in flist:
				result.append( ( f, ''))
			flist = result
			del result

		for (f, p) in flist:
			if f in self.__list:
				continue
			
			self.__list.append( (f, p ) )
		
		
		
		return self.__list
			
	def get (self, full = False):
		if not full:
			result = []
			for (f, p) in self.__list:
				result.append(f)
			
			return result

		return self.__list

	@staticmethod
	def check(flist, full = False):
		if isinstance(flist, FileList):
			flist = flist.get(True)
		elif isinstance(flist, str):
			flist = [(flist, '')]
		else:
			result = []
			for f in flist:
				result.append( ( f, ''))
			flist = result
			del result


		result = []
		for (f, p) in flist:
			if f.startswith('http'):

				f = PukeBuffer.fetchHttp(f)
			
			if not full:
				result.append(f)
			else:
				result.append((f, p))
      
		return result

	def __explore(self, dir ):
	    dir = os.path.abspath(dir)
	    for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
	        nfile = os.path.join(dir,file)
	        
	        if os.path.isdir(nfile):
	            self.__explore(nfile)
	        elif self.__filter.match(nfile) and not self.__exclude.match(nfile):
	        	tmp = nfile.split(self.__dir)
	        	if len(tmp) > 1:
	        		nfile = self.__dir + tmp[1]
	        	else:
	        		nfile = tmp[0]
	        	
	        	
	        	self.__list.append( (nfile, self.__dir))




class PukeBuffer:

	@staticmethod
	def fetchHttp(url):
		id = hashlib.sha256(url).hexdigest()

		if PukeBuffer.check(id):
			return PukeBuffer.getPath(id)
		
		try:
			handler = urllib2.build_opener()
			payload = handler.open(url).read()
		except Exception as error:
			console.error('HTTP fail %s (%s)' % (url, error))

		return PukeBuffer.write(id, payload, url)


	@staticmethod
	def write(id, payload, info = None):
		writefile(".pukecache/%s" % id, payload)

		if info:
			writefile(".pukecache/%s.meta" % id, info)

		return PukeBuffer.getPath(id)

	@staticmethod
	def check(id):
		return fileexists(".pukecache/%s" % id)

	@staticmethod
	def getPath(id):
		return ".pukecache/%s" % id

	@staticmethod
	def getInfo(id):
		if not fileexists(".pukecache/%s.meta" % id):
			return ""
		
		return readfile(".pukecache/%s.meta" % id)


	@staticmethod
	def clean():
		try:
			rm(".pukecache/")
			return True
		except:
			return False
		       