#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from prymatex.support import processor
from prymatex.support.syntax import PMXSyntax

class PMXSyntaxProcessor(processor.PMXSyntaxProcessor):
    def __init__(self, editor):
        self.editor = editor

    #START
    def startParsing(self, scope):
        self.setScopes([ scope ])
    
    #BEGIN NEW LINE
    def beginLine(self, line):
        self.line = line
        self.lineIndex = 0
        self.scopeRanges = []       #[ ((start, end), scopeHash) ... ]
        self.lineChunks = []        #[ ((start, end), chunk) ... ]
        self.words = []             #[ ((start, end), word, group) ... ]
        
    def endLine(self, line):
        self.addToken(len(self.line) + 1)

    #OPEN
    def openTag(self, scope, position):
        self.addToken(position)
        self.stackScopes.append(scope)

    #CLOSE
    def closeTag(self, scope, position):
        self.addToken(position)
        self.stackScopes.pop()
    
    #END
    def endParsing(self, scope):
        pass
    
    def setScopes(self, scopes):
        self.stackScopes = scopes

    def scopes(self):
        return self.stackScopes
        
    def addToken(self, end):
        begin = self.lineIndex
        # Solo si tengo realmente algo que agregar
        if begin != end:
            scopeHash, scopeGroup = self.editor.flyweightScopeFactory(self.stackScopes)
            self.scopeRanges.append( ((begin, end), scopeHash) )
            self.lineChunks.append( ((begin, end), self.line[begin:end]) )
            #TODO: Ver de sacar tambien los groups? y usar todo indexado por el scopeHash
            self.words += map(lambda match: ((begin + match.span()[0], begin + match.span()[1]), match.group(), scopeGroup), self.editor.RE_WORD.finditer(self.line[begin:end]))
        self.lineIndex = end
