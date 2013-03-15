#!/usr/bin/env python
# encoding: utf-8

from parser import Parser
from prymatex.support.utils import compileRegexp, OPTION_MULTILINE

class Format(object):
    def __init__(self, format):
        self.format = Parser.format(format)

    def apply(self, pattern, text, flags):
        return self.format.apply(pattern, text, flags)

class Transformation(object):
    def __init__(self):
        self.pattern = None
        self.format = None
        self.options = ""

    def setPattern(self, pattern):
        self.pattern = pattern
        
    def setFormat(self, format):
        self.format = Format(format)
        
    def setOptions(self, options):
        self.options = options
    
    def transform(self, text):
        pattern = compileRegexp(self.pattern, 'm' in self.options and OPTION_MULTILINE or None)
        return self.format.apply(pattern, text, self.options)
