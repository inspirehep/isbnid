#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hypatia: Module ISBN [isbn]
#

import re
from . import hyphen

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'

# ISBN: Internal ISBN13 string

ISBN10_RE = '(?P<isbn10>(\d(-| )?){9}(x|X|\d))'
ISBN10_NRE = '(\d(-| )?){9}(x|X|\d)'

ISBN13_RE = '(?P<isbn13>(\d(-| )?){12}(\d))'
ISBN13_NRE = '(\d(-| )?){12}(\d)'


def _normalize(str):
    if not re.match('^(\d(-| )?){9}(x|X|\d|(\d(-| )?){3}\d)$', str):
        raise ISBNError("Invalid ISBN format: {}".format(str))

    return re.sub('[^0-9X]', '', str.upper())


def _digit10(isbn):
    assert len(isbn) == 9
    product = 0
    for n in range(1, 10):
        product += int(isbn[n - 1]) * n
    return product % 11


def _digit13(isbn):
    assert len(isbn) == 12
    product = 0
    for n in range(0, 6):
        product += int(isbn[2 * n]) * 1
        product += int(isbn[2 * n + 1]) * 3
    return (- product) % 10

# hypenrng = hypen.HypenData('/home/elric/.nimbus/RangeMessage.xml')

# ISBN Structure
#
# Prefix Element: 978, 979      pre
# Registration Group Element    grp
# Registrant Element            reg
# Publication Element           pub
# Check Digit                   chk


class ISBNError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ISBN(object):

    hyphenRange = None

    def __init__(self, str):
        '''
        Creates ISBN object from a well formed ISBN string
        Raises exception if str is not a valid ISBN
        @type  str: string
        @param str: ISBN Number, either ISBN10 or ISBN13
        '''
        test = _normalize(str)
        self._id = None
        if len(test) == 13 and _digit13(test[:-1]) == int(test[12]):
            if test[0:3] != '978' and test[0:3] != '979':
                raise ISBNError("Invalid Bookland code: {}".format(test[0:3]))
            self._id = test
        if len(test) == 10:
            digit10 = _digit10(test[:-1])
            if digit10 == 10 and test[9] == 'X':
                self._id = '978' + test[:-1] + \
                    repr(_digit13('978' + test[:-1]))
            if test[9] != 'X' and digit10 == int(test[9]):
                self._id = '978' + test[:-1] + \
                    repr(_digit13('978' + test[:-1]))
        if not self._id:
            raise ISBNError("Invalid ISBN check digit: {}".format(str))

    def __str__(self):
        return self._id

    def hyphen(self):
        '''
        Returns ISBN number with segment hypenation
        Data obtained from https://www.isbn-international.org/
        https://www.isbn-international.org/export_rangemessage.xml
        @return: ISBN formated as ISBN13 with hyphens
        '''
        if not ISBN.hyphenRange:
            ISBN.hyphenRange = hyphen.ISBNRange()

        return ISBN.hyphenRange.hyphenformat(self._id)

    def isbn10(self):
        '''
        Encode ISBN number in ISBN10 format
        Raises exception if Bookland number different from 978
        @rtype:  string
        @return: ISBN formated as ISBN10
        '''
        if self._id[0:3] != '978':
            raise ISBNError("Invalid Bookland code: {}".format(self._id[0:3]))
        digit10 = _digit10(self._id[3:12])
        if digit10 == 10:
            return self._id[3:12] + 'X'
        else:
            return self._id[3:12] + str(digit10)

    def isbn13(self):
        '''
        Encode ISBN number in ISBN13 format (default encoding)
        @rtype:  string
        @return: ISBN formated as ISBN10
        '''
        return self._id

    def urn(self):
        '''
        ISBN URN RFC 3187
        @rtype:  string
        @return: ISBN formated as URN
        '''
        return 'URN:ISBN:{}'.format(self._id)

    def doi(self):
        '''
        Returns ISBN number with segment hypenation
        Data obtained from https://www.isbn-international.org/
        https://www.isbn-international.org/export_rangemessage.xml
        @return: ISBN formated as ISBN13 with hyphens
        '''
        if not ISBN.hyphenRange:
            ISBN.hyphenRange = hyphen.ISBNRange()

        seg = ISBN.hyphenRange.hyphensegments(self._id)
        return '10.' + self._id[0:3] + '.' + \
            self._id[3:-(1 + seg[3])] + '/' + self._id[-(1 + seg[3]):]

    @staticmethod
    def valid(str):
        try:
            id = ISBN(str)
        except:
            return False
        return True


def _doctest():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _doctest()
