#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# isbnid: Convert XMLRangeMessage.xml to Python code
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.3.1'

from xml.etree.ElementTree import ElementTree


class XML2PY(object):
    _range_grp = {}
    _range_reg = {}

    @staticmethod    
    def to13char(prefix):
        if(len(prefix)>=13):
            return(prefix[0:13])
        else:
            return(prefix + (prefix[-1] * (13 - len(prefix))))
    
    def __init__(self, xmlfile = None):
        tree = ElementTree()
        tree.parse(xmlfile)
        root = tree.getroot()
        
        self._serial = root[1].text
        self._date = root[2].text
        uccgrp = root[3]
        grpreg = root[4]
        
        for ucc in uccgrp:
            prefix = ucc[0].text
            for grp in ucc[2]:
                length = int(grp[1].text)
                start, end = grp[0].text.split('-')
                self._range_grp[prefix + start] = length
                self._range_grp[prefix + end] = length
                
        for grp in grpreg:
            prefix = grp[0].text.replace('-','')
            for reg in grp[2]:
                length = int(reg[1].text)
                start, end = reg[0].text.split('-')        
                self._range_reg[prefix + start] = length
                self._range_reg[prefix + end] = length                 
                
    def pycode(self):
        begin = None
        print('    _serial = "{}"'.format(self._serial))
        print('    _date = "{}"\n'.format(self._date))
        print('    _range_grp = [')
        for grp in sorted(self._range_grp.keys()):
            if grp[-1] != '9':
                begin = self.to13char(grp)[:]
            else:
                print("        ['{}', '{}', {}],".format(begin, self.to13char(grp)[:],self._range_grp[grp]))
        print('    ]\n')
        
        print('    _range_reg = [')
        for reg in sorted(self._range_reg.keys()):
            if reg[-1] != '9':
                begin = self.to13char(reg)[:]
            else:
                print("        ['{}', '{}', {}],".format(begin, self.to13char(reg)[:],self._range_reg[reg]))
        print('    ]\n')    
    
if __name__ == '__main__':

    print('''#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hypatia: Module ISBN Range [hyphen]
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.3.1'

# Interpretes current ISBN agency ranges
# Data obtained from https://www.isbn-international.org/
# https://www.isbn-international.org/export_rangemessage.xml

# ISBN Structure
#
# Prefix Element: 978, 979
# Registration Group Element
# Registrant Element
# Publication Element
# Check Digit
''')
    print(open('rtree.py').read())
    print('''
class ISBNRangeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

        
class ISBNRange(object):      
''')    
    xml2py = XML2PY('RangeMessage.xml')
    xml2py.pycode()
    print('''    _tree_grp = RangeList(_range_grp)
    _tree_reg = RangeList(_range_reg)
    
    def __init__(self, url = None): # url or filename
        pass

    @staticmethod
    def hyphensegments(isbn):
        grp = ISBNRange._tree_grp.search(isbn)
        reg = ISBNRange._tree_reg.search(isbn)          
        
        # pre, grp, reg, pub, chk

        pre = 3
        if not grp:
            raise ISBNRangeError(isbn)
        if not reg:
            raise ISBNRangeError(isbn)
                
        pub = 9 - grp - reg
        chk = 1
        
        return [pre, grp, reg, pub, chk]

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
      
''')

