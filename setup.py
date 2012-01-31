#!/usr/bin/env python
# -*- coding: utf8 -*-


from setuptools import setup, find_packages
import sys, os
import pkg_resources


major, minor = sys.version_info[:2]

if major < 2 and minor < 6:
    raise Exception("Puke requires Python 2.6")
import logging

setup(
    name = "puke",
    version = "1.5.5",
    packages = ['puke'],

    scripts = [
       'bin/puke',
       'bin/puke.js.compress',
       'bin/puke.css.compress'
    ],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['pyscss', 'closure_linter', 'colorama', 'pyyaml', 'paramiko'],
    dependency_links = ['http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz'],
  
    # metadata for upload to PyPI
    author = "Emmanuel Tabard",
    author_email = "manu@webitup.fr",
    description = "Puke is a straightforward build system",
    license = "http://www.gnu.org/copyleft/gpl.html",
    keywords = "build system python",
    url = 'http://github.com/webitup/puke',
    include_package_data = True
)