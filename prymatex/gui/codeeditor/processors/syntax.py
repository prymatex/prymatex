#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from prymatex.support import processor

class PMXSyntaxProcessor(processor.PMXSyntaxProcessor):
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
            