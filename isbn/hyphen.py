#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hypatia: Module ISBN Range [hyphen]
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.2.0'

try:
    from xml.etree.cElementTree import ElementTree
except ImportError:
    from xml.etree.ElementTree import ElementTree
    
import pkg_resources, sys


# Interpretes current ISBN agency ranges
# Data obtained from https://www.isbn-international.org/
# https://www.isbn-international.org/export_rangemessage.xml

class ISBNRangeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# ISBN Structure
#
# Prefix Element: 978, 979
# Registration Group Element
# Registrant Element
# Publication Element
# Check Digit

class ISBNRange(object):
    _range_grp = {}
    _range_reg = {}    

    def __init__(self, url = None): # url or filename
    
        if ISBNRange._range_grp and ISBNRange._range_reg:
            return
    
        et = ElementTree()
        if not url:
            rangefile = pkg_resources.resource_stream(__name__,'data/RangeMessage.xml')
            et.parse(rangefile)
        
        r = et.getroot()
        uccgrp = r[3]
        grpreg = r[4]

        for ucc in uccgrp:
            prefix = ucc[0].text
            for grp in ucc[2]:
                length = int(grp[1].text)
                start, end = grp[0].text.split('-')
                ISBNRange._range_grp[prefix + start] = length
                ISBNRange._range_grp[prefix + end] = length

        for grp in grpreg:
            prefix = grp[0].text.replace('-','')
            for reg in grp[2]:
                length = int(reg[1].text)
                start, end = reg[0].text.split('-')        
                ISBNRange._range_reg[prefix + start] = length
                ISBNRange._range_reg[prefix + end] = length   

        # assert 

    @staticmethod
    def hyphensegments(isbn):
        grp = reg = ''

        for igrp in sorted(ISBNRange._range_grp.keys()):
            if isbn <= igrp:
                break
            grp = igrp
        for ireg in sorted(ISBNRange._range_reg.keys()):
            if isbn <= ireg:
                break
            reg = ireg
            
        # pre, grp, reg, pub, chk

        pre = 3
        grp = ISBNRange._range_grp[grp]
        reg = ISBNRange._range_reg[reg]        
        pub = 9 - grp - reg
        chk = 1
        
        return [3, grp, reg, pub, 1]

    @staticmethod
    def hyphenformat(isbn):    
        pos = []
        start = 0
        
        for i in ISBNRange.hyphensegments(isbn):
            pos.append(isbn[start:start + i])
            start = start + i
            
        return '-'.join(pos)
        
def _doctest ():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _doctest()

