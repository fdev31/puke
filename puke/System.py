#!/usr/bin/env python
# -*- coding: utf8 -*-

import re, platform, os, pwd
from puke.ToolsExec import *
from distutils import version


try:
	LOGIN = pwd.getpwuid(os.getuid())[0]
except:
	LOGIN = None

_PLATFORM = OS = platform.system()
MACOS = "Darwin"
LINUX = "Linux"
WINDOWS = "Windows"

re_v = re.compile('((\d+)\.(\d+)(\.(\d+))?([ab](\d+))?)')
re_c = re.compile('(==|<=|>=|<|>)(.*)')

def check_package(name, compVersion = None, platform = "all"):

	if platform.lower() == LINUX.lower() and _PLATFORM != LINUX:
		return True
	
	if MACOS.lower() in platform.lower() and _PLATFORM != MACOS:
		return True

	check = sh("which %s" % name, header = None, output = False)
	check = check.strip()
	
	if not check:
		
		if _PLATFORM == MACOS:

			check = sh("brew info %s | grep -i -E \"(not installed|error)\"" % name, header=None, output=False)
			check = check.lower().strip()

			if "not installed" in check or 'error' in check:
				console.error('%s is M.I.A' % name)
				console.log(' => "brew install %s"' % name)
				console.error('')
				console.fail('%s not installed' % name)
		else:
			check = sh("aptitude show %s | grep -i -E \"(unable to locate|not installed)\"" % name, header=None, output=False)
			check = check.lower().strip()
			
			if "unable to locate" in check or 'not installed' in check:
				console.error('%s is M.I.A' % name)
				console.log(' => "aptitude install %s"' % name)
				console.error('')
				console.fail('%s not installed' % name)
		
		
	

	pVersion = get_package_version(name)

	goodVersion = True

	if compVersion:
		(op, wishVersion) = re_c.match(compVersion).groups()

		if op == "==":
			goodVersion = (version.StrictVersion(pVersion) == version.StrictVersion(wishVersion))
		elif op == "<=":
			goodVersion = (version.StrictVersion(pVersion) <= version.StrictVersion(wishVersion))
		elif op == ">=":
			goodVersion = (version.StrictVersion(pVersion) >= version.StrictVersion(wishVersion))
		elif op == "<":
			goodVersion = (version.StrictVersion(pVersion) < version.StrictVersion(wishVersion))
		elif op == ">":
			goodVersion = (version.StrictVersion(pVersion) > version.StrictVersion(wishVersion))
		else:
			console.fail('bad comp %s' % op)

	if goodVersion == True:
		console.confirm('%s : OK (%s)' % (name,pVersion))
	else:
		console.error('%s : OK (%s not %s)' % (name,pVersion, compVersion))

		console.fail('Failed on version comp %s ' % name)

	return True


def get_package_version(name, index = 0):
	check = ['--version', '-v', 'hard']

	if check[index] == 'hard':
		if _PLATFORM == MACOS:

			version = sh("toto='%s';test=`brew info $toto | grep -Ei '(?not installed|error)'`;\
							 if [[ -n \"$test\" ]]; then echo \"\"; else echo `brew info $toto | head -n 1`; fi" % (name), header = None, output = False)
		else:
			version = sh("toto='%s';test=`aptitude show $toto | grep -Ei '(?not installed|unable to locate)'`;\
							 if [[ -n \"$test\" ]]; then echo \"\"; else echo `aptitude show $toto | grep -i \"version:\"`; fi" % (name), header = None, output = False)
	else:
		version = sh('%s %s' % (name,check[index]), header = None, output = False, timeout=3)

	version = re_v.findall(version)
	if version:
		return version[0][0]
	elif len(check) <= index + 1:
		return "0.0"
	else:
		return get_package_version(name, index+1)
