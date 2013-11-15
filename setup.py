#!/usr/bin/python3
# -*- coding: utf8 -*-

from distutils.core import setup
setup(name='innodb-space',
      version='0.1',
      author='Daniël van Eeden',
      author_email='innodb-space@myname.nl',
      url='https://github.com/dveeden/innodb-space',
      description='InnoDB Table Space Monitoring',
      classifiers = [
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: POSIX",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Topic :: Database",
          "Topic :: System :: Monitoring",
          ],
      py_modules=['innodb_tablespace_info'],
      scripts=['innodb_check_free.py']
      )

