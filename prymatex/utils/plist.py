#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import re, plistlib
from string import printable

from . import encoding
from . import six

# FIX the string tags
def __fixString(sourceString):
    fixedString = ""
    index = fixStart = fixEnd = 0
    fixStart = sourceString.find("<string>", index)
    fixEnd = sourceString.find("</string>", fixStart)
    while fixStart != -1 and fixEnd != -1:
        fixedString += sourceString[index:fixStart]
        testString = sourceString[fixStart:fixEnd]
        if __shouldWrap(testString):
            testString = '<data>' + plistlib.Data(testString.encode("utf-8")).asBase64() + '</data>'
            fixEnd += 9
        fixedString += testString
        index = fixEnd
        fixStart = sourceString.find("<string>", index)
        fixEnd = sourceString.find("</string>", fixStart)
    fixedString += sourceString[index:]
    return fixedString
    
def __fixItems(dictionary, applyFunction):
    return dict(map(lambda item: (applyFunction(item[0]), applyFunction(item[1])), dictionary.items()))

def __fixWriteItem(item):
    if isinstance(item, dict):
        # Fix all the items in the dictionary
        return __fixItems(item, __fixWriteItem)
    elif isinstance(item, list):
        # Fix all items in the list
        return list(map(__fixWriteItem, item))
    elif isinstance(item, six.string_types):
        # Fix any unicode or non-printable strings
        return __wrapItem(item)
    return item

def __fixReadItem(item):
    if isinstance(item, dict):
        # Fix all the items in the dictionary
        return __fixItems(item, __fixReadItem)
    elif isinstance(item, list):
        # Fix all items in the list
        return list(map(__fixReadItem, item))
    elif isinstance(item, plistlib.Data):
        return item.data.decode("utf-8")
    elif isinstance(item, six.string_types):
        # Return unicode in python 2
        return six.text_type(item)
    return item

def __wrapItem(item):
    if __shouldWrap(item):
        return plistlib.Data(item.encode("utf-8"))
    else:
        return item

def __shouldWrap(string):
    return not set(string).issubset(set(printable)) \
        or __containsUnicode(string)

def __containsUnicode(string):
    try:
        string.encode('ascii')
        return False
    except:
        return True

if six.PY3:
    # Monkey patch
    plistlib.readPlistFromString = lambda data: \
        plistlib.readPlistFromBytes(data.encode("utf-8"))
    plistlib.writePlistToString = lambda data: \
        plistlib.writePlistToBytes(data).decode("utf-8")
        
def readPlist(filePath):
    try:
        data = plistlib.readPlist(filePath)
    except Exception as e:
        # Solo si tiene error
        data = plistlib.readPlistFromString(__fixString(encoding.read(filePath)[0]))
    return __fixItems(data, __fixReadItem)

def writePlist(dictionary, filePath):
    plistlib.writePlist(__fixItems(dictionary, __fixWriteItem), filePath)
    
def readPlistFromString(string):
    try:
        data = plistlib.readPlistFromString(string)
    except Exception as e:
        # Solo si tiene error
        data = plistlib.readPlistFromString(__fixString(string))
    return __fixItems(data, __fixReadItem)
    
def writePlistToString(dictionary):
    return plistlib.writePlistToString(__fixItems(dictionary, __fixWriteItem))
