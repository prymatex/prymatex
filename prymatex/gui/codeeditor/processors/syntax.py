#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from copy import copy

from prymatex.support import processor

RE_WORD = re.compile(r"([A-Za-z_]\w+\b)", re.UNICODE)

class PMXSyntaxProcessor(processor.PMXSyntaxProcessor):
    def __init__(self, editor):
        self.editor = editor

    #START
    def startParsing(self, scope):
        self.setScopes([ scope ])
    
    #BEGIN NEW LINE
    def beginLine(self, line, stack):
        self.line = line
        self.lineIndex = 0
        self.scopes = []         #[ s0, s1, .... sN ]
        self.scopeRanges = []       #[ ((start, end), scope) ... ]
        self.preferences = []       #[ ((start, end), preference) ... ]
        self.lineChunks = []        #[ ((start, end), chunk) ... ]
        self.words = []             #[ ((start, end), word) ... ]
        self.state = None
        
    def endLine(self, line, stack):
        self.addToken(len(self.line) + 1)
        if len(stack) != 1:
            self.state = (copy(stack), copy(self.stackScopes))

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
        
    def addToken(self, end):
        begin = self.lineIndex
        # Solo si tengo realmente algo que agregar
        if begin != end:
            scope = " ".join(self.stackScopes)
            self.scopes[begin:end] = [scope for _ in xrange(end - begin)]
            self.scopeRanges.append( ((begin, end), scope) )
            self.preferences.append( ((begin, end), self.editor.preferenceSettings(scope)) )
            chunk = self.line[begin:end]
            self.lineChunks.append( ((begin, end), chunk) )
            self.words += map(lambda match: ((begin + match.span()[0], begin + match.span()[1]), match.group()), RE_WORD.finditer(chunk))
        self.lineIndex = end
