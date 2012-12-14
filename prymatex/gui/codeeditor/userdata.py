#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

from prymatex.support.syntax import PMXSyntax

class CodeEditorBlockUserData(QtGui.QTextBlockUserData):
    def __init__(self):
        QtGui.QTextBlockUserData.__init__(self)
        # Indent and content
        self.indent = ""
        
        self.textHash = None
        
        self.__blank = True
        self.__scopeRanges = []
        self.__lineChunks = []
        self.__cache = {}

    
    def __nonzero__(self):
        return bool(self.__scopeRanges)
    
    
    def setScopeRanges(self, ranges):
        self.__scopeRanges = ranges
    
    
    def scopeRanges(self, start = None, end = None):
        ranges = self.__scopeRanges[:]
        if start is not None:
            ranges = filter(lambda range: range[0][0] >= start, ranges)
        if end is not None:
            ranges = filter(lambda range: range[0][1] <= end, ranges)
        return ranges
    
    
    def setLineChunks(self, chunks):
        self.__lineChunks = chunks
        
        
    def lineChunks(self):
        return self.__lineChunks[:]
        
        
    def setBlank(self, blank):
        self.__blank = blank
    
    
    def blank(self):
        return self.__blank
        
        
    def getLastScope(self):
        return self.__scopeRanges[-1][1]
        
    def scopeAtPosition(self, pos):
        return self.scopeRange(pos)[1]
    
    def scopeRange(self, pos):
        ranges = self.scopeRanges()
        sr = filter(lambda ((start, end), scope): start <= pos <= end, self.__scopeRanges)
        return sr[0] if len(sr) >= 1 else ((0, 0), None)
    
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
        return map(lambda scopeRange: scopeRange[0], filter(lambda scopeRange: groupFilter(scopeRange[1]), self.__scopeRanges))

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
        return self.__cache.get("processor_state")

    def setProcessorState(self, processorState):
        self.__cache["processor_state"] = processorState

    def saveState(self):
        return {}
        
    def restoreState(self, state):
        pass