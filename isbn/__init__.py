#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hypatia: Module ISBN [__init__]
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.2.1'

from . isbn import ISBN, ISBNError

__all__ = ['ISBN', 'ISBNError',
    'ISBN10_RE', 'ISBN10_NRE', 'ISBN13_RE', 'ISBN13_NR'
    ]
