#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from copy import copy
from PyQt4 import QtCore, QtGui
from prymatex.support import PMXSyntaxProcessor, PMXSyntax, PMXPreferenceSettings

WHITESPACE = re.compile(r'^(?P<whitespace>\s+)', re.UNICODE)
def whiteSpace(text):
    match = WHITESPACE.match(text)
    try:
        ws = match.group('whitespace')
        return ws
    except AttributeError:
        return ''

# Syntax
class PMXBlockUserData(QtGui.QTextBlockUserData):
    INDENT_NONE = PMXPreferenceSettings.INDENT_NONE
    INDENT_INCREASE = PMXPreferenceSettings.INDENT_INCREASE
    INDENT_DECREASE = PMXPreferenceSettings.INDENT_DECREASE
    INDENT_NEXTLINE = PMXPreferenceSettings.INDENT_NEXTLINE
    UNINDENT = PMXPreferenceSettings.UNINDENT
    
    def __init__(self, scopes = []):
        QtGui.QTextBlockUserData.__init__(self)
        self.scopes = scopes
        self.foldingMark = PMXSyntax.FOLDING_NONE
        self.foldedLevel = 0
        self.folded = False
        self.indentMark = self.INDENT_NONE
        self.indent = ""
        self.textHash = None
        self.cache = None

    def __nonzero__(self):
        return bool(self.scopes)
    
    def getLastScope(self):
        return self.scopes[-1]
    
    def setScopes(self, scopes):
        self.scopes = scopes
        
    def getScopeAtPosition(self, pos):
        return self.scopes[pos]
    
    def getAllScopes(self, start = 0, end = None):
        current = ( self.scopes[start], start ) if start < len(self.scopes) else ("", 0)
        end = end or len(self.scopes)
        scopes = []
        for index, scope in enumerate(self.scopes[start:], start):
            if scope != current[0]:
                scopes.append(( current[0], current[1], index ))
                current = ( scope, index )
        scopes.append(( current[0], current[1], end ))
        return scopes
    
    def getStackAndScopes(self):
        return copy(self.cache[0]), copy(self.cache[1])
    
    def setStackAndScopes(self, stack, scopes):
        self.cache = (stack, scopes)

class PMXProcessor(PMXSyntaxProcessor):
    #START
    def startParsing(self, scope):
        self.lines = []
        self.setScopes([ scope ])
    
    #BEGIN NEW LINE
    def beginLine(self, line, stack):
        self.line = line
        self.lineIndex = 0
        self.lines.append([[], None])
        
    def endLine(self, line, stack):
        self.addToken(len(self.line) + 1)
        if len(stack) != 1:
            #Save the stack and scopes
            self.lines[-1][1] = (copy(stack), copy(self.scopes)) 

    #OPEN
    def openTag(self, scope, position):
        self.addToken(position)
        self.scopes.append(scope)

    #CLOSE
    def closeTag(self, scope, position):
        self.addToken(position)
        self.scopes.pop()
    
    #END
    def endParsing(self, scope):
        pass
    
    def setScopes(self, scopes):
        self.scopes = scopes
        
    def addToken(self, end):
        begin = self.lineIndex
        # Solo tengo realmente algo que agregar
        if begin != end:
            scopes = " ".join(self.scopes)
            self.lines[-1][0][begin:end] = [scopes for _ in xrange(end - begin)]
        self.lineIndex = end
        
class PMXSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    NO_STATE = -1
    SINGLE_LINE = 0
    MULTI_LINE = 1
    FORMAT_CACHE = {}
    
    def __init__(self, editor):
        self.editor = editor
        self.processor = PMXProcessor()
        self.__syntax = None
        self.__formatter = None
        self.future = None
        super(PMXSyntaxHighlighter, self).__init__(self.editor.document())

    @property
    def syntax(self):
        return self.__syntax
    
    @syntax.setter
    def syntax(self, syntax):
        self.__syntax = syntax
        self.editor.document().blockSignals(True)
        self.future = self.editor.pmxApp.executor.submit(self._analyze_all_text, self.editor.toPlainText())
        self.future.add_done_callback(self._on_analyze_ready)
        
    @property
    def formatter(self):
        return self.__formatter

    @formatter.setter
    def formatter(self, formatter):
        self.__formatter =  formatter
        #Deprecate format cache
        self.__formatter.clearCache()
        PMXSyntaxProcessor.FORMAT_CACHE = {}
        if self.future == None or not self.future.running():
            self.rehighlight()
    
    def _on_analyze_ready(self, future):
        self.editor.document().blockSignals(False)
        self.rehighlight()
        
    def _analyze_all_text(self, text):
        self.syntax.parse(text, self.processor)
        for index, data in enumerate(self.processor.lines):
            block = self.editor.document().findBlockByNumber(index)
            userData, state = self.buildBlockUserData(block, data)
            block.setUserData(userData)
            block.setUserState(state)
    
    def applyFormat(self, userData):
        #Formatear
        for scope, start, end in userData.getAllScopes():
            format = self.getFormat(scope)
            if format is not None:
                self.setFormat(start, end - start, format)
    
    def buildBlockUserData(self, block, data):
        userData = block.userData()
        state = self.SINGLE_LINE
        if userData is None:
            userData = PMXBlockUserData(data[0])
        else:
            userData.setScopes(data[0])
        if data[1] is not None:
            state = self.MULTI_LINE
            userData.setStackAndScopes(*data[1])
        
        text = block.text()
        #Folding
        userData.foldingMark = self.syntax.folding(text)
        userData.textHash = hash(text)
        
        #Indent
        settings = self.editor.getPreference(self.syntax.scopeName)
        userData.indentMark = settings.indent(text)
        userData.indent = whiteSpace(text)
        return userData, state
        
    def highlightBlock(self, text):
        #Start Parsing
        block_number = self.currentBlock().blockNumber()
        userData = self.currentBlock().userData()
        
        if userData != None and userData.textHash == hash(text):
            self.applyFormat(userData)
        else:
            self.processor.startParsing(self.syntax.scopeName)
            if self.previousBlockState() == self.MULTI_LINE:
                #Recupero una copia del stack y los scopes del user data
                stack, scopes = self.currentBlock().previous().userData().getStackAndScopes()
                self.processor.setScopes(scopes)
            else:
                #Creo un stack y scopes nuevos
                stack = [[self.syntax.grammar, None]]
    
            # A parserar mi amor, vamos a parsear mi amor
            self.syntax.parseLine(stack, text, self.processor)
            
            data = self.processor.lines[-1]
            userData, state = self.buildBlockUserData(self.currentBlock(), data)
            self.setCurrentBlockUserData(userData)
            self.setCurrentBlockState(state)
            self.applyFormat(userData)
        
    def getFormat(self, scope):
        if self.formatter == None: return None
        if scope not in PMXSyntaxProcessor.FORMAT_CACHE:
            format = QtGui.QTextCharFormat()
            settings = self.formatter.getStyle(scope)
            if 'foreground' in settings:
                format.setForeground(settings['foreground'])
            if 'background' in settings:
                format.setBackground(settings['background'])
            if 'fontStyle' in settings:
                if 'bold' in settings['fontStyle']:
                    format.setFontWeight(QtGui.QFont.Bold)
                if 'underline' in settings['fontStyle']:
                    format.setFontUnderline(True)
                if 'italic' in settings['fontStyle']:
                    format.setFontItalic(True)
            PMXSyntaxProcessor.FORMAT_CACHE[scope] = format 
        return PMXSyntaxProcessor.FORMAT_CACHE[scope]
        