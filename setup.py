#!/usr/bin/env python3

import sys
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
       'bin/puke'
      ],
      
      data_files = [
        ("doc", [
          "readme"
        ])
      ]
)
