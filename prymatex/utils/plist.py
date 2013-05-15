#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import sys
import re, plistlib
from string import printable

XMLPATTERN = re.compile("<(\w+)>(.*)<\/\w+>");

if sys.version_info.major < 3:
    str = unicode

# FIX, FIX, FIX
def __fixItems(dictionary, applyFunction):
    return dict(map(lambda item: (applyFunction(item[0]), applyFunction(item[1])), dictionary.items()))

def __fixWriteItem(item):
    if isinstance(item, dict):
        # Fix all the items in the dictionary
        item = __fixItems(item, __fixWriteItem)
    elif isinstance(item, list):
        # Fix all items in the list
        item = list(map(__fixWriteItem, item))
    elif isinstance(item, str):
        # Fix any unicode or non-printable strings
        item = __wrapItem(item)
    return item

def __fixReadItem(item):
    if isinstance(item, dict):
        # Fix all the items in the dictionary
        item = __fixItems(item, __fixReadItem)
    elif isinstance(item, list):
        # Fix all items in the list
        item = list(map(__fixReadItem, item))
    elif isinstance(item, plistlib.Data):
        item = item.data.decode("utf-8")
    return item

def __wrapItem(item):
    if __shouldWrap(item):
        return plistlib.Data(bytes(item, "utf-8"))
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

if sys.version_info.major >= 3:
    # Monkey patch
    plistlib.readPlistFromString = lambda data: \
        plistlib.readPlistFromBytes(bytes(data, "utf-8"))
  
def readPlist(filePath):
    try:
        data = plistlib.readPlist(filePath)
    except Exception as e:
        result = []
        start = 0
        data = open(filePath).read()
        if sys.version_info.major < 3:
            data = data.decode("utf-8")
        for match in XMLPATTERN.finditer(data):
            if __shouldWrap(match.group(2)):
                result.append(data[start:match.start()])
                item = b'<data>' + plistlib.Data(match.group(2).encode("utf-8")).asBase64() + b'</data>'
                result.append(item.decode("utf-8"))
                start = match.end()
        result.append(data[start:])
        result = "".join(result)
        if sys.version_info.major < 3:
            result = result.encode("utf-8")
        data = plistlib.readPlistFromString(result)
    return __fixItems(data, __fixReadItem)
    
def writePlist(dictionary, filePath):
    plistlib.writePlist(__fixItems(dictionary, __fixWriteItem), filePath)
    
if __name__ == "__main__":
    testFile = "/mnt/datos/workspace/Prymatex/prymatex/prymatex/share/Bundles/ShellScript.tmbundle/Commands/man.plist"
    datos = readPlist(testFile)
    print(datos)
