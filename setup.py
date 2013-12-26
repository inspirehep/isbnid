#!/usr/bin/env python

from distutils.core import setup, Extension

# digit = Extension('isbn.digit', sources = ['isbn/digitmodule.c'])
# chyphen = Extension('isbn.chyphen', sources = ['isbn/chyphenmodule.c'])

setup(name = 'isbnid',
    version = '0.2.2',
    description = "Python ISBN ids",
    license = "LGPL",
    url = 'http://code.google.com/p/isbnid/',
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Indexing",
        ],
    packages = ['isbn'],
    package_dir = {'isbn': 'isbn'},
    package_data = {'isbn': ['data/*.xml']}
    )
    

