#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from PyQt4 import QtGui
from prymatex.support.syntax import PMXSyntax

class PMXBlockUserData(QtGui.QTextBlockUserData):
    def __init__(self):
        QtGui.QTextBlockUserData.__init__(self)
        self.scopes = []
        #Folding
        self.foldingMark = PMXSyntax.FOLDING_NONE
        self.foldedLevel = 0
        self.folded = False
        #Indent
        self.indent = ""
        #Symbols
        self.symbol = None
        self.textHash = None
        self.cache = None

    def __nonzero__(self):
        return bool(self.scopes)
    
    def getLastScope(self):
        return self.scopes[-1]
    
    def setScopes(self, scopes):
        self.scopes = scopes
        
    def getScopeAtPosition(self, pos):
        #FIXME: Voy a poner algo mentiroso si pos no esta en self.scopes
        scope = self.scopes[pos] if pos < len(self.scopes) else self.scopes[-1]
        return scope
    
    def getScopeRange(self, pos):
        ranges = self.getScopeRanges()
        range = filter(lambda (scope, start, end): start <= pos <= end, ranges)
        assert len(range) >= 1, "More than one range"
        range = range[0] if len(range) == 1 else None
        return range
    
    #Deprecated name, use getScopeRanges
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
    
    def getScopeRanges(self, start = 0, end = None):
        return self.getAllScopes(start, end)
    
    #================================================
    # Cache Handle
    #================================================
    def getStackAndScopes(self):
        return copy(self.cache[0]), copy(self.cache[1])
    
    def setStackAndScopes(self, stack, scopes):
        self.cache = (stack, scopes)
