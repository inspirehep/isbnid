isbnid
======

Python ISBN identifier library

isbnid is a simple library to handle ISBN identification numbers. isbnid will store, check and convert ISBNs in ISBN10, and ISBN13 formats and it will transform between them and output in URN form.

isbnid can also output ISBN numbers with the correct hyphens corresponding to the actual issuance authorities. The information is retrieved from <https://www.isbn-international.org/>. ISBN numbers have a complex internal structure which roughly represents the country, the language and the publisher. See also <https://en.wikipedia.org/wiki/ISBN>.

Install
-------

isbnid has no dependences. The simplest way to install it in python is to execute. 

    pip install isbnid

It can also be installed from source as

    python setup.py install

isbnid is source compatible with both Python 2 and Python 3.

Usage
-----

The class isbn.ISBN constructor takes a string containing the ISBN. The string can be inputed in ISBN10, ISBN13 with or without hyphens. It will raise an exception in case it is not formated correctly or the check digit is not valid.

    >>> import isbn
    >>> isbnid = isbn.ISBN("9780553109535")
    >>> isbnid.isbn10()
    '0553109537'
    >>> isbnid.isbn13()
    '9780553109535'
    >>> isbnid.urn()
    'URN:ISBN:9780553109535'
    >>> isbnid.hyphen()
    '978-0-553-10953-5'
    >>> isbnid = isbn.ISBN("978-0-553-10953-0")
    isbn.isbn.ISBNError: 'Invalid ISBN check digit: 978-0-553-10953-0'
  
