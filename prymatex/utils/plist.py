#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import re, plistlib
from string import printable

from . import six

XMLPATTERN = re.compile("<(\w+)>(.*)<\/\w+>");

# FIX, FIX, FIX
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
    return six.text_type(item)

def __wrapItem(item):
    if __shouldWrap(item):
        return plistlib.Data(item.encode("utf-8"))
    else:
        return item.encode("utf-8")

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
  
def readPlist(filePath):
    try:
        data = plistlib.readPlist(filePath)
    except Exception as e:
        result = []
        start = 0
        data = open(filePath).read()
        if not six.PY3:
            data = data.decode("utf-8")
        for match in XMLPATTERN.finditer(data):
            if __shouldWrap(match.group(2)):
                result.append(data[start:match.start()])
                item = b'<data>' + plistlib.Data(match.group(2).encode("utf-8")).asBase64() + b'</data>'
                result.append(item.decode("utf-8"))
                start = match.end()
        result.append(data[start:])
        result = "".join(result)
        if not six.PY3:
            result = result.encode("utf-8")
        data = plistlib.readPlistFromString(result)
    return __fixItems(data, __fixReadItem)
    
def writePlist(dictionary, filePath):
    plistlib.writePlist(__fixItems(dictionary, __fixWriteItem), filePath)
    
if __name__ == "__main__":
    testFile = "/mnt/datos/workspace/Prymatex/prymatex/prymatex/share/Bundles/ShellScript.tmbundle/Commands/man.plist"
    datos = readPlist(testFile)
    print(datos)
