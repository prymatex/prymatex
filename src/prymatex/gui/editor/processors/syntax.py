#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from copy import copy
from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData
from prymatex.support import PMXSyntaxProcessor, PMXSyntax, PMXPreferenceSettings

from logging import getLogger
logger = getLogger(__file__)

WHITESPACE = re.compile(r'^(?P<whitespace>\s+)', re.UNICODE)
def whiteSpace(text):
    match = WHITESPACE.match(text)
    try:
        ws = match.group('whitespace')
        return ws
    except AttributeError:
        return ''

# Syntax
class PMXBlockUserData(QTextBlockUserData):
    FOLDING_NONE = PMXSyntax.FOLDING_NONE
    FOLDING_START = PMXSyntax.FOLDING_START
    FOLDING_STOP = PMXSyntax.FOLDING_STOP
    INDENT_NONE = PMXPreferenceSettings.INDENT_NONE
    INDENT_INCREASE = PMXPreferenceSettings.INDENT_INCREASE
    INDENT_DECREASE = PMXPreferenceSettings.INDENT_DECREASE
    INDENT_NEXTLINE = PMXPreferenceSettings.INDENT_NEXTLINE
    UNINDENT = PMXPreferenceSettings.UNINDENT
    
    def __init__(self):
        QTextBlockUserData.__init__(self)
        self.scopes = []
        self.foldingMark = self.FOLDING_NONE
        self.foldedLevel = 0
        self.folded = False
        self.indentMark = self.INDENT_NONE
        self.indent = ""
        self.cache = None

    def __nonzero__(self):
        return bool(self.scopes)
    
    def getLastScope(self):
        return self.scopes[-1]
    
    def addScope(self, begin, end, scope):
        self.scopes[begin:end] = [scope for _ in xrange(end - begin)]
        
    def getScopeAtPosition(self, pos):
        return self.scopes[pos]
    
    def getAllScopes(self, start = 0, end = None):
        current = ( self.scopes[start], start )
        scopes = []
        for index, scope in enumerate(self.scopes[start:], start):
            if scope != current[0] or (end != None and index == end):
                scopes.append(( current[0], current[1], index ))
                current = ( scope, index )
                if end != None and index == end:
                    break
        return scopes
    
    def getStackAndScopes(self):
        return copy(self.cache[0]), copy(self.cache[1])
    
    def setStackAndScopes(self, stack, scopes):
        self.cache = (stack, scopes)
    
class PMXSyntaxProcessor(QSyntaxHighlighter, PMXSyntaxProcessor):
    SINGLE_LINE = 0
    MULTI_LINE = 1
    FORMAT_CACHE = {}
    
    def __init__(self, editor):
        QSyntaxHighlighter.__init__(self, editor.document())
        self.editor = editor
        self.__syntax = None
        self.__formatter = None

    def getSyntax(self):
        return self.__syntax
    def setSyntax(self, syntax):
        self.__syntax =  syntax
        self.rehighlight()
    syntax = property(getSyntax, setSyntax)
    
    def getFormatter(self):
        return self.__formatter
    def setFormatter(self, formatter):
        self.__formatter =  formatter
        #Deprecate format cache
        self.__formatter.clearCache()
        PMXSyntaxProcessor.FORMAT_CACHE = {}
        self.rehighlight()
    formatter = property(getFormatter, setFormatter)

    def highlightBlock(self, text):
        #Start Parsing
        self.block_number = self.currentBlock().blockNumber()
        self.userData = self.currentBlock().userData()
        if self.userData == None:
            self.editor.folding.insert(self.block_number)
            self.userData = PMXBlockUserData()
            self.setCurrentBlockUserData(self.userData)
        
        text = unicode(text)
        if self.previousBlockState() == self.MULTI_LINE:
            #Recupero una copia del stack y los scopes del user data
            stack, self.scopes = self.currentBlock().previous().userData().getStackAndScopes()
        else:
            #Creo un stack y scopes nuevos 
            stack = [[self.syntax.grammar, None]]
            self.scopes = [ self.syntax.scopeName ]
        # A parserar mi amor, vamos a parsear mi amor
        self.syntax.parseLine(stack, text, self)
        
        #End Parsing
        self.addToken(self.currentBlock().length())
        if self.scopes[-1] == self.syntax.scopeName:
            self.setCurrentBlockState(self.SINGLE_LINE)
        else:
            self.setCurrentBlockState(self.MULTI_LINE)
            self.userData.setStackAndScopes(stack, self.scopes)
            
        line = unicode(self.currentBlock().text())
        self.foldingMarker(line)
        self.indentMarker(line, self.scopes[-1])

    def addToken(self, end):
        begin = self.line_position
        # Solo si no estoy descartando lineas y tengo realmente algo que agregar
        if begin != end:
            scopes = " ".join(self.scopes)
            self.userData.addScope(begin, end, scopes)
            format = self.getFormat(scopes)
            if format is not None:
                self.setFormat(begin, end - begin, format)
            #preferences = self.editor.getPreference(scopes)
            #if preferences is not None:
            #    pass
        self.line_position = end
    
    def getFormat(self, scope):
        if self.formatter == None: return None
        if scope not in PMXSyntaxProcessor.FORMAT_CACHE:
            PMXSyntaxProcessor.FORMAT_CACHE[scope] = self.formatter.getStyle(scope).QTextFormat
        return PMXSyntaxProcessor.FORMAT_CACHE[scope]
    
    #===============================================================================
    # PMXSyntaxProcessor interface
    #===============================================================================
    #NEW LINE
    def newLine(self, line):
        self.line_position = 0

    #OPEN
    def openTag(self, scope, position):
        self.addToken(position)
        self.scopes.append(scope)

    #CLOSE
    def closeTag(self, scope, position):
        self.addToken(position)
        self.scopes.pop()
        
    #===============================================================================
    # Extra data for user data
    #===============================================================================
    def foldingMarker(self, line):
        self.userData.foldingMark = self.syntax.folding(line)
        if self.userData.foldingMark == PMXBlockUserData.FOLDING_START:
            self.editor.folding.setOpen(self.block_number)
        elif self.userData.foldingMark == PMXBlockUserData.FOLDING_STOP:
            self.editor.folding.setClose(self.block_number)
        elif self.userData.foldingMark == PMXBlockUserData.FOLDING_NONE:
            self.editor.folding.setNone(self.block_number)

    def indentMarker(self, line, scope):
        settings = self.editor.getPreference(scope)
        self.userData.indentMark = settings.indent(line)
        if self.syntax.indentSensitive and line.strip() == "":
            prev = self.currentBlock().previous()
            self.userData.indent = prev.userData().indent if prev.isValid() else ""
        else: 
            self.userData.indent = whiteSpace(line)