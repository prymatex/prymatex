#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################### SyntaxProcessor #################################

class PMXSyntaxProcessor(object):
    '''
        Syntax Processor, clase base para los procesadores de sintaxis
    '''
    def __init__(self):
        pass

    def open_tag(self, name, position):
        pass

    def close_tag(self, name, position):
        pass

    def new_line(self, line):
        pass

    def start_parsing(self, name):
        pass

    def end_parsing(self, name):
        pass

class PMXDebugSyntaxProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.line_number = 0
        self.printable_line = ''

    def pprint(self, line, string, position = 0):
        line = line[:position] + string + line[position:]
        return line

    def open_tag(self, name, position):
        print self.pprint( '', '{ %d - %s' % (position, name), position + len(self.line_marks))

    def close_tag(self, name, position):
        print self.pprint( '', '} %d - %s' % (position, name), position + len(self.line_marks))

    def new_line(self, line):
        self.line_number += 1
        self.line_marks = '[%04s] ' % self.line_number
        print '%s%s' % (self.line_marks, line)

    def start_parsing(self, name):
        print '{%s' % name

    def end_parsing(self, name):
        print '}%s' % name
