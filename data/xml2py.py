#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# isbnid: Convert XMLRangeMessage.xml to Python code
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.3.0'

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
        print('    _range_grp = {')
        for grp in sorted(self._range_grp.keys()):
            if grp[-1] != '9':
                print('        "{}": {},'.format(self.to13char(grp)[:],self._range_grp[grp]))
        print('    }\n')
        
        print('    _range_reg = {')
        for reg in sorted(self._range_reg.keys()):
            if reg[-1] != '9':
                print('        "{}": {},'.format(self.to13char(reg)[:],self._range_reg[reg]))
        print('    }')    
    
if __name__ == '__main__':
    print('''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hypatia: Module ISBN Range [hyphen]
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.3.0'

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
''')      
    xml2py = XML2PY('RangeMessage.xml')
    xml2py.pycode()
    print('''
    def __init__(self, url = None): # url or filename
        pass

    @staticmethod
    def hyphensegments(isbn):
        grp = None
        reg = None

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
        if not grp or isbn > igrp: # None or 0
            raise ISBNRangeError(isbn)
        grp = ISBNRange._range_grp[grp]
        if not reg or isbn > ireg: # None or 0
            raise ISBNRangeError(isbn)
                
        reg = ISBNRange._range_reg[reg]        
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

