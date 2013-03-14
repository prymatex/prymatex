#!/usr/bin/env python
# encoding: utf-8

from parser import Parser

class Transformation(object):
    def __init__(self, regexp, format, options = []):
        self.regexp = regexp
        self.format = []
        Parser(format).parse_format_string("", self.format)
        self.options = options

if __name__ == '__main__':
    t = Transformation("\A<em>(.*)<\em>\z|.*","(?1:$1:<em>$0<em>)", "m")
    print t.format