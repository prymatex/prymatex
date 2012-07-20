#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from prymatex.support.syntax import PMXSyntax
from prymatex.utils.decorators.deprecated import deprecated

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
        #Words
        self.words = []

        self.textHash = None
        
        self.__cache = {}

    def __nonzero__(self):
        return bool(self.scopes)
    
    def setScopes(self, scopes):
        self.scopes = scopes
        
    def setRanges(self, ranges):
        self.ranges = ranges
        
    def setPreferences(self, preferences):
        self.preferences = preferences
    
    def setChunks(self, chunks):
        self.chunks = chunks
        
    def getLastScope(self):
        return self.scopes[-1]
        
    def scopeAtPosition(self, pos):
        return self.scopes[pos]
        
    @deprecated
    def getScopeAtPosition(self, pos):
        #FIXME: Voy a poner algo mentiroso si pos no esta en self.scopes
        scope = self.scopes[pos] if pos < len(self.scopes) else self.scopes[-1]
        return scope
    
    def scopeRange(self, pos):
        ranges = self.scopeRanges()
        sr = filter(lambda ((start, end), scope): start <= pos <= end, self.ranges)
        assert len(sr) >= 1, "More than one range"
        sr = sr[0] if len(sr) == 1 else None
        return sr
    
    def scopeRanges(self, start = None, end = None):
        ranges = self.ranges[:]
        if start is not None:
            ranges = filter(lambda range: range[0][0] >= start, ranges)
        if end is not None:
            ranges = filter(lambda range: range[0][1] <= end, ranges)
        return ranges
    
    def isWordInScopes(self, word):
        return word in reduce(lambda scope, scope1: scope + " " + scope1[1], self.scopeRanges(), "")

    def groups(self, nameFilter):
        #http://manual.macromates.com/en/language_grammars
        # 11 root groups: comment, constant, entity, invalid, keyword, markup, meta, storage, string, support, variable
        def groupFilter(scope):
            names = nameFilter.split()
            accepted = True
            for name in names:
                if name[0] == "-":
                    name = name[1:]
                    accepted = accepted and all(map(lambda s: not s.startswith(name), scope.split()))
                else:
                    accepted = accepted and any(map(lambda s: s.startswith(name), scope.split()))
            return accepted
        return map(lambda scopeRange: scopeRange[0], filter(lambda scopeRange: groupFilter(scopeRange[1]), self.ranges))

    def wordsByGroup(self, nameFilter):
        groups = self.groups(nameFilter)
        return filter(lambda word: any(map(lambda group: group[0] <= word[0][0] and group[1] >= word[0][1], groups)), self.words)

    def wordsRanges(self, start = None, end = None):
        words = self.words[:]
        if start is not None:
            words = filter(lambda ran: ran[0][0] >= start, words)
        if end is not None:
            words = filter(lambda ran: ran[0][1] <= end, words)
        return words

    #================================================
    # Cache Handle
    #================================================
    def processorState(self):
        return self.__cache["processor_state"]

    def setProcessorState(self, processorState):
        self.__cache["processor_state"] = processorState

    def saveState(self):
        return {}
        
    def restoreState(self, state):
        pass