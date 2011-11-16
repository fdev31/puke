

"""REquire parser

This class simply provide an accessor on a dict
"""


'''generic:
	titi: "dtc"

dev:
	toto: "${BOURSE_PATH}|/toto/coucou"
	titi: "${BOURSE_PATH}|/toto/coucou"
	coin:
		toto: 'cul'




c = Require("mesbourses.yaml")



#c.merge("toto.yaml")
c.makevars('generic')
-> titi, valeur dtc
c.makevars('dev')
-> titi, jgjg

#make_glob(c.get('dev'))

global toto
global titi

toto = c.get('dev')['toto']
titi = c.get('dev')['titi']

coin = [toto: vf,;:]





CONFIG['toto']'''

import os,re
import yaml,json
from puke.Env import *
from puke.Console import *
from puke.Yak import *



class Require(object):

	__sharedState = {}
	__globalPattern = re.compile('\$\{([^}]+)\}[|]?(.*)')


	def __init__(self, filename):
		self.__dict__ = self.__sharedState
		if not self.__sharedState:
			self.__files = [filename]
			self.__cfg = self.__load(filename)
			self.__makeenvs(self.__cfg)
			

	def merge(self, filename):
		self.__files.append(filename)
		self.__cfg.update(self.__load(filename))
		self.__makeenvs(self.__cfg)

	def yak(self, selector):
		for (node, value) in self.get(selector).items():			
			Yak.set(node,value)
		
		

	def get(self, key):
		if self.__cfg.has_key(key):
			return self.__cfg[key]

	def set(self, key, value):
		self.__cfg[key] = value

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key, value):
		self.set(key, value)

	def __contains__(self, key):
		return (key in self.__cfg)

	def __repr__(self):
		return 'Config: %s' % self.__cfg

	def __load(self, filename):
		try:
			stream = None
			stream = file(filename, 'r')
			ext = os.path.splitext(stream.name)[1]

			result = None

			if ext in ['.json', '.js']:
				result = json.loads(stram)
			elif ext in ['.yaml', '.yml']:
				result = yaml.load(stream)

			
		except Exception as error :
			raise RequireError("Require load error : %s" % error)
			result = None
		finally:
			if stream:
				stream.close()

		return result
	
	def __makeenvs(self, data ):	
		if isinstance(data, list):
			dataIter = enumerate(data)
		else:
			dataIter = data.items()
		
		for (node, value) in dataIter:
			if not isinstance(value, str):
				self.__makeenvs(value)
			elif value.startswith('${'):
				m = self.__globalPattern.match(value)
				if not m:
					continue
				
				(name, default) = m.groups()
				value = Env.get(name, default)
				data[node] = value
				

	def reload(self):
		files = self.__files
		self.__files = []
		self.__cfg = {}
		for filename in files:
			self.include(filename)

class RequireError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
