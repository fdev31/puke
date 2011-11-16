#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

major, minor = sys.version_info[:2]

if major < 2 and minor < 6:
    raise Exception("Puke requires Python 2.6")
import logging

setup(
    name = "puke",
    version = "1.1.1",
    packages = ['puke'],

    scripts = [
       'bin/puke',
       'bin/puke.js.compress',
       'bin/puke.css.compress',
       'bin/puke.js.runner'
    ],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['pyscss', 'closure_linter', 'colorama', 'PyYAML'],
    dependency_links = ['http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz'],
  
    # metadata for upload to PyPI
    author = "Emmanuel Tabard",
    author_email = "manu@webitup.fr",
    description = "Puke is a straightforward build system",
    license = "http://www.apache.org/licenses/LICENSE-2.0",
    keywords = "build system python",
    url = 'http://github.com/roxee/puke',
    include_package_data = True
)
