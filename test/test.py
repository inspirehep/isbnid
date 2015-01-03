#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hypatia: Module ISBN Test [test]
#

__author__ = "Neko"
__license__ = 'LGPL http://www.gnu.org/licenses/lgpl.txt'
__version__ = '0.3.2'

import unittest

import isbn

# Add incorrect 979 ISBN10 Fail
# Add valid digit incorrect Bookland code

isbn_ok = {
    '012345672X':    ['012345672X', '9780123456724', '978-0-12-345672-4'],
    '9780387308869': ['0387308865', '9780387308869', '978-0-387-30886-9'],
    '9780393334777': ['0393334775', '9780393334777', '978-0-393-33477-7'],
    '9781593273880': ['1593273886', '9781593273880', '978-1-59327-388-0'],
    '9788478447749': ['8478447741', '9788478447749', '978-84-7844-774-9'],
    }

isbn_nok = {
    'X123456781',
    '012345678X',
    '9780123456780',
    '9780123456781',
    '9790123456780',
    '9790123456781',
    '9890123456781'
    }


class ISBNTest(unittest.TestCase):

    def testISBNIn(self):
        for book in isbn_nok:
            self.assertFalse(isbn.ISBN.valid(book))
    
    def testISBNOut(self):
        for book in sorted(isbn_ok.keys()):
            id = isbn.ISBN(book)
            self.assertEqual(id.isbn10(), isbn_ok[book][0])
            self.assertEqual(id.isbn13(), isbn_ok[book][1])
        
    def testHyphen(self):
        for book in sorted(isbn_ok.keys()):
            id = isbn.ISBN(book)
            self.assertEqual(id.hyphen(), isbn_ok[book][2])

if __name__ == '__main__':
    unittest.main()
