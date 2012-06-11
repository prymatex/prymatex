#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os
from functools import partial

RE_SHELL_VAR = re.compile('(\$[\w\d]+)')

def callback(match, context = None, sensitive = True, default = ''):
    key = match.group().replace('$', '')
    if callable(context):
        context = context()
    if not sensitive:
        return context.get(key.lower(), context.get(key.upper(), default))
    else:
        return context.get(key, default)

environ_repl_callback = partial(callback, sensitive = False, context = os.environ)

#===============================================================================
# Expand $exp taking os.environ as context
#===============================================================================
expand_shell_var = lambda path: RE_SHELL_VAR.sub(path, environ_repl_callback)

def fullsplit(path, result=None):
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
        return os.path.normpath(p) + os.sep
    return fixpath(childPath).startswith(fixpath(parentPath))

if __name__ == "__main__":
    print os.sep
    print expand_shell_var("$PATH/alfa")