#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os
from functools import partial

RE_SHELL_VAR = re.compile('\$([\w\d]+)')

def callback(match, context = None, sensitive = True, default = ''):
    key = match.group(1)
    if sensitive:
        return context.get(key, default)
    else:
        return context.get(key.lower(), context.get(key.upper(), default))

#===============================================================================
# Expand $exp taking os.environ as context
#===============================================================================
def expand_shell_var(path, context = None, sensitive = True):
    if context is not None and callable(context):
        context = context()
    elif context is None:
        context = os.environ
    
    return RE_SHELL_VAR.sub(partial(callback, sensitive = sensitive, context = context), path)

def fullsplit(path, result = None):
    """
    Split a pathname into components (the opposite of os.path.join) in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

def issubpath(childPath, parentPath):
    def fixpath(p):
        return os.path.normcase(p) + os.sep
    return fixpath(childPath).startswith(fixpath(parentPath))

if __name__ == "__main__":
    print issubpath("c:\cygwin\home\dvanhaaster\workspace\prymatex\prymatex\utils\osextra\path.py", "C:/cygwin/home/dvanhaaster/workspace/prymatex")
    print expand_shell_var("$PATH/alfa")