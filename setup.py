#!/usr/bin/env python

from distutils.core import setup

from isbn import __version__

setup(
    name = 'isbnid_fork',
    version = __version__,
    author = 'ISBNid GitHub',
    author_email = 'admin@inspirehep.net',
    description = "Python ISBN ids",
    license = "GPL",
    url = 'https://github.com/inspirehep/isbnid',
    keywords = 'ISBN',
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Indexing",
        ],
    packages = ['isbn'],
    package_dir = {'isbn': 'isbn'},
    )
