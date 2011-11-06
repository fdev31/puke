#!/usr/bin/env python3

from setuptools import setup, find_packages
import sys

major, minor = sys.version_info[:2]

#if major < 3:
#    raise Exception("Puke requires Python 3")

setup(
    name = "puke",
    version = "0.1",
    packages = find_packages(),
    scripts = [
       'bin/puke',
       'bin/puke.js.compress',
       'bin/puke.css.compress'
    ],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Emmanuel Tabard",
    author_email = "manu@webitup.fr",
    description = "Puke is a straightforward build system",
    license = "http://www.apache.org/licenses/LICENSE-2.0",
    keywords = "build system python",
    url = 'http://github.com/roxee/puke',   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)


'''import sys
from distutils.core import setup

major, minor = sys.version_info[:2]

if major < 3:
    raise Exception("Puke requires Python 3")

version = "0.1"

setup(
      name = 'puke',
      version = version,
      
      author = 'Emmanuel Tabard',
      author_email = 'contact@webitup.fr',
      
      url = 'http://github.com/roxee/puke',
      download_url = "http://github.com/downloads/roxee/puke/puke-%s.tar.gz" % version,
      
      license = "http://www.apache.org/licenses/LICENSE-2.0",
      
      description = "Puke is a straightforward build system",
      long_description = "",

      packages = [
        'puke'
      ],
      
      package_dir = {
        '': 'lib'
      },
      
      package_data = {
        'puke': [
         
        ]
      },
      
      scripts = [
       'bin/puke',
       'bin/puke.js.compress',
       'bin/puke.css.compress'
      ],
      
      data_files = [
        ("doc", [
          "readme"
        ])
      ]
)'''
