#!/usr/bin/env python
# encoding: utf-8

from parser import Parser

class Format(object):
    def __init__(self, format):
        self.format = format and Parser.format(format)

if __name__ == '__main__':
    f = Format("(?1:$1:<em>$0<em>)")
    print f.format