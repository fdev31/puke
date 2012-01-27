#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, logging
import fnmatch, re
import hashlib



from puke.Console import *
from puke.FileSystem import *
from puke.Cache import *



class FileList:

	__gExclude = ''

	def __init__(self, dir, filter = "*", exclude = ""):
		self.__list = []
		self.__dir = os.path.abspath(dir)
		self.__filter = ""


		if dir.startswith('http') or dir.startswith('ftp'):
			self.__list.append((dir,''))
			return


		for tmp_f in filter.split(','):
			tmp_f = tmp_f.strip(' ')
			self.__filter = "%s|(%s)" % (self.__filter, fnmatch.translate(tmp_f))
		
		self.__filter = self.__filter.strip('|')
		self.__filter = re.compile(self.__filter)
		
		self.__exclude = FileList.__gExclude
		for tmp_f in exclude.split(','):
			tmp_f = tmp_f.strip(' ')
			self.__exclude = "%s|(%s)" % (self.__exclude, fnmatch.translate(tmp_f))
		
		self.__exclude = self.__exclude.strip('|')
		self.__exclude = re.compile(self.__exclude)



		self.__explore(dir)

	@staticmethod
	def addGlobalExclude(rule):
		FileList.__gExclude = "%s|(%s)" % (FileList.__gExclude, fnmatch.translate(rule))

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
	def getSignature(list):
		sig = ""
		for (f,p) in list:
			sig += "%s" % hashlib.sha256(f).hexdigest()
		
		sig = hashlib.sha256(sig).hexdigest()

		return sig

	@staticmethod
	def check(flist, full = False):
		if isinstance(flist, FileList):
			flist = flist.get(True)
		elif isinstance(flist, str):

			try:
				cIsFile = isfile(flist)
			except:
				cIsFile = False
				
			flist = [(flist, '')] if cIsFile else FileList(flist).get(True)
		else:
			result = []
			for f in flist:
				result.append( ( f, ''))
			flist = result
			del result


		result = []
		for (f, p) in flist:
			if f.startswith('http') or f.startswith('ftp'):

				f = Cache.fetchHttp(f)
			
			if not full:
				result.append(f)
			else:
				result.append((f, p))
      
		return result

	def __explore(self, dir ):
	    dir = os.path.abspath(dir)
	    for file in sorted([file for file in os.listdir(dir) if not file in [".",".."]]):
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





		       