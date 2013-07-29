#!/usr/bin/env python

from .parser import parse_format_string
from . import types
from .base import compileRegexp

class String(object):
    def __init__(self, source):
        self.nodes = parse_format_string(source)
        
    def __str__(self):
        return "".join([unicode(node) for node in self.nodes])

    __unicode__ = __str__
    
    def replace(self, source, pattern, repeat = False, variables = None):
        memodict = {}
        pattern = compileRegexp(pattern)
        match = pattern.search(source)
        if match:
            text = source[:match.start()]
            while match:
                text += "".join([node.replace(memodict, match = match, variables = variables) for node in self.nodes])
                if not repeat:
                    break
                match = pattern.search(source, match.end())
            text += source[match.end():]
            return text
    
    def escape(self):
        pass

    def expand(self, match = None, variables = None):
        return "".join([node.replace({}, match = match, variables = variables) for node in self.nodes])

    def substitute(self, source, variables = None):
        return self.replace(source, ".+")