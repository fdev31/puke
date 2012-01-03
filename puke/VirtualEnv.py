#!/usr/bin/env python
# -*- coding: utf8 -*-

from puke.Tools import *
from puke.ToolsExec import *
from puke.FileSystem import *
import System
from distutils import version

import os


re_v = re.compile('((\d+)\.(\d+)(\.(\d+))?([ab](\d+))?)')
re_c = re.compile('(==|<=|>=|<|>)?(.*)')

class VirtualEnv(object):
	def __init__(self):
		self.__path = None

	def load (self, path):
		self.__path = path

	def create(self, path, python = "python", force = False):

		console.header(' * Creating env "%s" ...' % (path))
		if not force and exists(os.path.join(path, 'bin', 'activate')):
			self.__path = path
			console.confirm('   Env "%s" already created. Use "force=True" to override it' % path)
			return True

		check = System.check_package('virtualenv')
		version = System.get_package_version(python)
		console.log('   Python version : %s ...' % version)

		

		result = sh("virtualenv -p %s %s --no-site-packages " % (python, path), header = False, output = False)
		console.debug(result)

		console.confirm('   Env "%s"  created' % path)
		self.__path = path


	def install(self, package, whishVersion = None, upgrade = False):
		if not self.__path:
			raise VirtualEnvError('Need load|create before install')

		if not upgrade:
			console.header(' * Install "%s" in env "%s" ...' % (package, self.__path))
		else:
			console.header(' * Upgrade "%s" in env "%s" ...' % (package, self.__path))

		opts = []

		if upgrade == True:
			opts.append('--upgrade')

		cmd = [
			'source %s' % os.path.join(self.__path, 'bin', 'activate'),
			'pip install %s %s' % (package if not whishVersion else package+"=="+whishVersion, " ".join(opts))
		]
		result = sh(cmd, header = False, output = False)
		console.debug(result)

		console.confirm('   Package "%s" is ready' % package)

	def upgrade(self, package = "*"):

		if package == "*":
			packages = self.list(output = False)
		else:
			packages = [(package, 0)]

		for (package, v) in packages:
			self.install(package, True)

	def check_package(self, package, compVersion = None, fix = False):

		console.header('  * Check package "%s" %s ' % (package, compVersion))

		infos = self.package_info(package, output = False)

		op = wishVersion = None
		if compVersion:
			
			if compVersion.lower() != "latest":
				(op, wishVersion) = re_c.match(compVersion).groups()

			compVersion = compVersion.lower()

		if not infos:
			console.error('    No package')

			if fix:
				console.log('   Fixing ...')
				self.install(package, wishVersion)
				return True
			else:
				return False
		else:
			(name, cVersion, lVersion) = infos


		if compVersion and compVersion != "latest":
			goodVersion = False
			if op == "==":
				goodVersion = (version.StrictVersion(cVersion) == version.StrictVersion(wishVersion))
			elif op == "<=":
				goodVersion = (version.StrictVersion(cVersion) <= version.StrictVersion(wishVersion))
			elif op == ">=":
				goodVersion = (version.StrictVersion(cVersion) >= version.StrictVersion(wishVersion))
			elif op == "<":
				goodVersion = (version.StrictVersion(cVersion) < version.StrictVersion(wishVersion))
			elif op == ">":
				goodVersion = (version.StrictVersion(cVersion) > version.StrictVersion(wishVersion))
			else:
				console.fail('   bad comparator %s (eg : >=1.6)' % op)			

			if not goodVersion:

				if op == ">":
					wishVersion = lVersion

				console.error('    Wrong version %s VS %s' % (cVersion, wishVersion))

				if fix:
					console.log('   Fixing ...')
					return self.install(package, wishVersion, upgrade = True)
				else:
					return False

			else:
				console.confirm(' Everything is ok (Current %s, Last %s)' % (cVersion, lVersion))
				return True

		elif compVersion == "latest":
			if (version.StrictVersion(cVersion) == version.StrictVersion(lVersion)):
				console.confirm('    This is the latest package')
				return True
			else:
				console.warn('    Package needs an upgrade %s => %s' % (cVersion, lVersion))
				if fix:
					console.log('   Fixing ...')
					return self.install(package, wishVersion, upgrade = True)
				else:
					return False
		else:
			console.confirm('    Everything is ok (Current %s, Last %s)' % (cVersion, lVersion))

		return True

		


	def package_info(self, package, output = True):

		if output:
			console.header('  * Package "%s" :' % package)
		
		package = package.lower().strip()
		installed_packages = self.list(output = False)

		here = False
		info = {}
		for (p, v) in installed_packages:
			if package != p.lower().strip():
				continue
			else:
				here = True
				info['name'] = p
				info['version'] = v
				break
		
		if not here:
			if output:
				console.error('    No package "%s"' % package)
			return False
		
		#get last version
		cmd = [
			'source %s' % os.path.join(self.__path, 'bin', 'activate'),
			'pip search %s | grep "LATEST:" | head -n 1' % package
		]
		result = sh(cmd, header = False, output = False)

		last = re_v.findall(result)
		if last:
			last = last[0][0]
		else:
			last = info['version']

		if output:
			

			if last != "0.0" and last != info['version']:
				console.confirm('    - Current Version %s' % info['version'])
				console.warn('    - Latest Version %s ' % last)
			else:
				console.confirm('    - Current Version %s (latest)' % info['version'])

		return (info['name'], info['version'], last)


	def list(self, output = True):
		if not self.__path:
			raise VirtualEnvError('Need load|create before install')
		
		cmd = [
			'source %s' % os.path.join(self.__path, 'bin', 'activate'),
			'pip freeze'
		]

		if output:
			console.header(' * List packages (env \"%s\")' % self.__path)


		result = sh(cmd, header = False, output = False)
		
		lines = result.split('\n')


		packages = []
		for line in lines:
			if line == "":
				continue

			extract = line.rsplit('==', 1)
			if len(extract) == 1:
				name = extract[0]
				version = 0
			else:
				(name, version) = extract

			if output:
				console.info('   - %s (%s)' % (name, version))

			packages.append((name, version))
		
		return packages
	
	def remove(self):
		 if not self.__path or not exists(os.path.join(self.__path, 'bin', 'activate')):
		 	raise VirtualEnvError('"%s" is not a python env')
		 
		 console.header(' * Deleting env \"%s\" ... ' % self.__path)
		 rm(self.__path)
		 console.confirm('   Env "%s" deleted' % self.__path)



class VirtualEnvError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
