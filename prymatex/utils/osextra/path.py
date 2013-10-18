#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os
from functools import partial
import collections

from prymatex.utils import six

RE_SHELL_VAR = re.compile('\$([\w\d]+)')

#===============================================================================
# Expand $exp taking os.environ as context
#===============================================================================
def expand_shell_variables(path, context=None, sensitive=True):
    
    # Get context
    if six.callable(context):
        context = context()
    elif context is None:
        context = os.environ
    
    if not sensitive:
        context = dict([(key.upper(), value) for key, value in context.items()])

    def callback(match, context = None, sensitive = True):
        key = match.group(1)
        value = context.get(key) if sensitive else context.get(key.upper())
        return value or "$%s" % key
    
    return RE_SHELL_VAR.sub(partial(callback, context = context, sensitive = sensitive), path)

def ensure_not_exists(path, name, suffix = 0):
    """Return a safe path, ensure not exists"""
    if suffix == 0 and not os.path.exists(path % name):
        return path % name
    else:
        newPath = path % (name + "_" + six.text_type(suffix))
        if not os.path.exists(newPath):
            return newPath
        else:
            return ensure_not_exists(path, name, suffix + 1)

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

def issubpath(childPath, parentPath, normpath = True, realpath = False):
    def fixpath(p):
        path = os.path.normcase(p)
        path = normpath and os.path.normpath(path) or path
        path = realpath and os.path.realpath(path) or path
        return path + os.sep
    return fixpath(childPath).startswith(fixpath(parentPath))

if __name__ == "__main__":
    print(issubpath("\\cygwin\\home\\dvanhaaster\\workspace\\prymatex\\prymatex\\utils\\osextra\\path.py", "/cygwin/home/dvanhaaster/workspace/prymatex"))
    print(issubpath("/home/diego/workspace/Prymatex/prymatex/setup.py", "/mnt/datos/workspace/Prymatex/prymatex", realpath=True))
    print(expand_shell_variables("$PATH/alfa"))