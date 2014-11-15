#!/usr/bin/env python

from distutils.core import setup, Extension

# digit = Extension('isbn.digit', sources = ['isbn/digitmodule.c'])
# chyphen = Extension('isbn.chyphen', sources = ['isbn/chyphenmodule.c'])

setup(
    name = 'isbnid',
    version = '0.3.0',
    author = 'ISBNid GitHub',
    author_email = 'pdfnorm@gmx.com',
    description = "Python ISBN ids",
    license = "LGPL",
    url = 'https://github.com/nekobcn/isbnid',
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
    )
    

