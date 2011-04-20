#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################### SyntaxProcessor #################################

class PMXSyntaxProcessor(object):
    '''
        Syntax Processor, clase base para los procesadores de sintaxis
    '''
    def __init__(self):
        pass

    def openTag(self, name, position):
        pass

    def closeTag(self, name, position):
        pass

    def newLine(self, line):
        pass

    def startParsing(self, name):
        pass

    def endParsing(self, name):
        pass

class PMXDebugSyntaxProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.line_number = 0
        self.printable_line = ''

    def pprint(self, line, string, position = 0):
        line = line[:position] + string + line[position:]
        return line

    def openTag(self, name, position):
        print self.pprint( '', '{ %d - %s' % (position, name), position + len(self.line_marks))

    def closeTag(self, name, position):
        print self.pprint( '', '} %d - %s' % (position, name), position + len(self.line_marks))

    def newLine(self, line):
        self.line_number += 1
        self.line_marks = '[%04s] ' % self.line_number
        print '%s%s' % (self.line_marks, line)

    def startParsing(self, name):
        print '{%s' % name

    def endParsing(self, name):
        print '}%s' % name

class PMXCommandProcessor(object):
    '''
        Syntax Processor, clase base para los procesadores de sintaxis
    '''
    def __init__(self):
        pass

    # Inputs
    def getDocument(self):
        pass
    def getCharacter(self):
        pass
    def getDocument(self):
        pass
    # Outpus function
    def discard(self):
        pass
    def replaceSelectedText(self):
        pass
    def replaceDocument(self):
        pass
    def insertText(self):
        pass
    def afterSelectedText(self):
        pass
    def insertAsSnippet(self):
        pass
    def showAsHTML(self):
        pass
    def showAsTooltip(self):
        pass
    def createNewDocument(self):
        pass
