#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# isbnid: Convert XMLRangeMessage.xml to Rust code
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.4.4'

import email.utils

from xml.etree.ElementTree import ElementTree


class XML2RS(object):
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
        self._sdate = root[2].text
        self._tdate = email.utils.parsedate(self._sdate)
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

    def rscode_grp(self):
        begin = None
        '''
        print('    _serial = "{}"'.format(self._serial))
        print('    _sdate = "{}"'.format(self._sdate))
        print('    _tdate = {}\n'.format(self._tdate))
        print('    _range_grp = [')
        '''
        
        print("static RANGE_GRP: [(&'static str, &'static str, usize); {}] = [".format(int(len(self._range_grp) / 2)))
        for grp in sorted(self._range_grp.keys()):
            if grp[-1] != '9':
                begin = self.to13char(grp)[:]
            else:
                print("    (\"{}\", \"{}\", {}), ".format(begin, self.to13char(grp)[:], self._range_grp[grp]))
        
    def rscode_reg(self):
        begin = None        
        
        print("static RANGE_REG: [(&'static str, &'static str, usize); {}] = [".format(int(len(self._range_reg) / 2)))
        for reg in sorted(self._range_reg.keys()):
            if reg[-1] != '9':
                begin = self.to13char(reg)[:]
            else:
                print("    (\"{}\", \"{}\", {}), ".format(begin, self.to13char(reg)[:], self._range_reg[reg]))
                
        

if __name__ == '__main__':
    xrs = XML2RS('RangeMessage.xml')
    print('''///! Auto generated from RangeMessage.xml

''')
    xrs.rscode_grp()
    print('''];
''')
    XML2RS('RangeMessage.xml').rscode_reg()        
    print('''];

fn bisect(range: &[(&'static str, &'static str, usize)], id: &str) -> usize {
    let mut lo: usize = 0;
    let mut hi: usize = range.len() ;
    let mut mid;

    while lo < hi {
        mid = (lo + hi) / 2;
        let (start, _, _) = range[mid];
        if id < start {
            hi = mid
        } else {
            lo = mid + 1
        }
    }
    range[lo - 1].2
}

pub fn segments(id: &str) -> (usize, usize, usize) {
    let grp = bisect(&RANGE_GRP, id);
    let reg = bisect(&RANGE_REG, id);
    
    if grp == 0 || reg == 0 {
        (0, 0, 0)
    } else {
        (grp, reg, 9 - grp - reg)
    }
}    


''')    

