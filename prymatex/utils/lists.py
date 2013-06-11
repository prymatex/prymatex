#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from bisect import bisect

def bisect_key(elements, element, key = lambda x: x):
    indexs = list(map(key, elements))
    index = key(element)
    return bisect(indexs, index)

def FIXMEbisect(elements, element, function):
    #FIXME: No funciona
    if not elements:
        return 0
    else:
        index = len(elements) / 2
        comp = function(elements[index], element)
        if comp > 0:
            index = index - 1 if index > 0 else 0
            return index + bisect(elements[:index], element, function)
        elif comp < 0:
            index = index + 1 if index < len(elements) else len(elements)
            return index + bisect(elements[index:], element, function)
        else:
            return index
