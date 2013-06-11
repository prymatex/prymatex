#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui

from functools import reduce

CodeEditorBlockUserDataToken = namedtuple("CodeEditorBlockUserDataToken", [
    "start", "end", "scopeHash", "chunk"
])

class CodeEditorBlockUserData(QtGui.QTextBlockUserData):

    def __init__(self):
        QtGui.QTextBlockUserData.__init__(self)
        self.textHash = None
        
        self.__blank = True
        self.__tokens = []
        self.__scopeRanges = []
        self.__lineChunks = []
        self.__cache = {}

    def setTokens(self, tokens):
        self.__tokens = tokens
        self.__scopeRanges = [ ((token.start, token.end), token.scopeHash) for token in tokens ]
        self.__lineChunks = [ ((token.start, token.end), token.chunk) for token in tokens ]

    def tokens(self, start = None, end = None):
        tokens = self.__tokens
        if start is not None:
            tokens = [ token for token in tokens if token.start >= start ]
        if end is not None:
            tokens = [ token for token in tokens if token.end <= end ]
        return tokens

    def scopeRanges(self, start = None, end = None):
        ranges = self.__scopeRanges[:]
        if start is not None:
            ranges = [ range for range in ranges if range[0][0] >= start ]
        if end is not None:
            ranges = [ range for range in ranges if range[0][1] <= end ]
        return ranges

    def lineChunks(self):
        return self.__lineChunks[:]

    def setBlank(self, blank):
        self.__blank = blank
    
    def blank(self):
        return self.__blank
        
    def lastToken(self):
        return self.__tokens[-1]
        
    def lastScope(self):
        return self.__scopeRanges[-1][1]

    def tokenAtPosition(self, pos):
        for token in self.__tokens[::-1]:
            if token.start <= pos <= token.end:
                return token

    def scopeAtPosition(self, pos):
        return self.scopeRange(pos)[1]
    
    def scopeRange(self, pos):
        sr = [start_end_scope for start_end_scope in self.__scopeRanges if start_end_scope[0][0] <= pos < start_end_scope[0][1]]
        return sr and sr.pop() or ((-1,-1), None)
    
    def __isWordInScopes(self, word):
        return word in reduce(lambda scope, scope1: scope + " " + scope1[1], self.scopeRanges(), "")

    def __groups(self, nameFilter):
        #http://manual.macromates.com/en/language_grammars
        # 11 root groups: comment, constant, entity, invalid, keyword, markup, meta, storage, string, support, variable
        def groupFilter(scope):
            names = nameFilter.split()
            accepted = True
            for name in names:
                if name[0] == "-":
                    name = name[1:]
                    accepted = accepted and all([not s.startswith(name) for s in scope.split()])
                else:
                    accepted = accepted and any([s.startswith(name) for s in scope.split()])
            return accepted
        return [scopeRange[0] for scopeRange in [scopeRange for scopeRange in self.__scopeRanges if groupFilter(scopeRange[1])]]

    def __wordsByGroup(self, nameFilter):
        groups = self.groups(nameFilter)
        return [word for word in self.words if any([group[0] <= word[0][0] and group[1] >= word[0][1] for group in groups])]

    def __wordsRanges(self, start = None, end = None):
        words = self.words[:]
        if start is not None:
            words = [ran for ran in words if ran[0][0] >= start]
        if end is not None:
            words = [ran for ran in words if ran[0][1] <= end]
        return words

    # ------------------- Cache Handle
    def processorState(self):
        return self.__cache.get("processor_state", ([], []))

    def setProcessorState(self, processorState):
        self.__cache["processor_state"] = processorState

    def saveState(self):
        return {}
        
    def restoreState(self, state):
        pass
