#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# isbnid: Convert XMLRangeMessage.xml to C code
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.2.0'

from xml.etree.ElementTree import ElementTree


class XML2C(object):
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
                
    def ccode(self):
        print('char *grpkey[] = {')
        for grp in sorted(self._range_grp.keys()):
            if grp[-1] != '9':
                print('    "{}",'.format(self.to13char(grp)[:]))
        print('};\n') 
        
        print('int grprng[] = {')     
        for grp in sorted(self._range_grp.keys()):
            if grp[-1] != '9':        
                print('    {},'.format(self._range_grp[grp]))
        print('};\n')
        
        print('char *regkey[] = {')
        for reg in sorted(self._range_reg.keys()):
            if reg[-1] != '9':
                print('    "{}",'.format(self.to13char(reg)[:]))
        print('};\n')    

        print('int regrng[] = {')     
        for reg in sorted(self._range_reg.keys()):
            if reg[-1] != '9':
                print('    {},'.format(self._range_reg[reg]))
        print('};')
    
if __name__ == '__main__':
    
    xml2c = XML2C('RangeMessage.xml')
    print('#include <Python.h>\n')
    xml2c.ccode()
    print(
'''
static PyMethodDef hyrmMethods[] = {
    {"range", hyrm_range, METH_VARARGS, "ISBN ranges"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hyrmmodule = {
   PyModuleDef_HEAD_INIT,
   "hyrm",   /* name of module */
   NULL, //hyrm_doc, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   hyrmMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&hyrmmodule);
}
    
const char *isbnid;
    
static PyObject*      
    hyrm_range(PyObject* self, PyObject* isbn)}
    if (!PyArg_ParseTuple(isbn, "s", &isbnid))
        return NULL;
    return(PyBuild_Value("ii", group, range))
};
''' 
)      